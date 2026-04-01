from pathlib import Path
from typing import List, Tuple
import re

class KnowledgeChunk:
    def __init__(self, text: str, topic: str):
        self.text = text
        self.topic = topic

def load_knowledge(base_path: str = "../data") -> List[KnowledgeChunk]:
    chunks: List[KnowledgeChunk] = []
    folder = Path(base_path)
    if not folder.exists():
        return chunks
    for path in folder.glob("*.md"):
        topic = path.stem
        text = path.read_text(encoding="utf-8")
        for para in text.split("\n\n"):
            para = para.strip()
            if len(para) > 80:
                chunks.append(KnowledgeChunk(para, topic))
    return chunks

knowledge_chunks = load_knowledge()

def retrieve_relevant(query: str, top_k: int = 4) -> List[KnowledgeChunk]:
    if not knowledge_chunks:
        return []
    
    # Very simple keyword-based ranking (lightweight TF-IDF approximation)
    words = set(re.findall(r'\w+', query.lower()))
    
    scored_chunks = []
    for chunk in knowledge_chunks:
        chunk_words = chunk.text.lower()
        score = sum(1 for w in words if w in chunk_words and len(w) > 3)
        # If the chunk topic matches a keyword, give it a big boost
        if any(w in chunk.topic.lower() for w in words if len(w) > 3):
            score += 5
        scored_chunks.append((score, chunk))
        
    # Sort by score descending and take top_k (even 0-score chunks are fine if we need context)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in scored_chunks[:top_k]]

def build_answer(user_profile: dict, query: str, history: List[str]) -> Tuple[str, List[str]]:
    retrieved = retrieve_relevant(query)
    topics = list({c.topic for c in retrieved if c.topic})

    intro_parts = []
    if user_profile.get("is_smoker"):
        intro_parts.append("Note: Because you smoke, your risk of heart and lung disease is higher.")
    if user_profile.get("has_hypertension"):
        intro_parts.append("Note: You mentioned high blood pressure, so controlling salt and stress is important.")
    if user_profile.get("has_diabetes"):
        intro_parts.append("Note: With diabetes, healthy diet and regular follow-up visits are very important.")

    red_flags = ["chest pain", "severe headache", "difficulty breathing"]
    if any(flag in query.lower() for flag in red_flags):
        emergency = (
            "You mentioned a serious symptom. Please go to the nearest clinic "
            "or emergency service immediately. Do not rely on chatbot advice only. "
        )
        return emergency, ["emergency"]

    context_knowledge = ""
    if retrieved:
        context_knowledge = "\n\nRelevant Excerpts from Knowledge Base:\n" + "\n".join(c.text for c in retrieved)

    from app.config import settings
    import google.generativeai as genai
    from .prompts import PULSE_HEALTH_AI_PROMPT

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return (
            "[SYSTEM NOTIFICATION: The AI backend GEMINI_API_KEY is not configured.]\n\n"
            + "".join(intro_parts) + "\n\n" + (context_knowledge if retrieved else "No context found.")
        ), topics

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=PULSE_HEALTH_AI_PROMPT
    )

    user_prompt = f"User Profile Considerations: {' '.join(intro_parts)}\n" if intro_parts else ""
    user_prompt += context_knowledge + "\n\n"
    user_prompt += f"Chat History:\n" + "\n".join([f"User: {msg}" if i % 2 == 0 else f"AI: {msg}" for i, msg in enumerate(history)]) + "\n\n"
    user_prompt += f"Current Question: {query}\n\nPlease respond based on your instructions."

    try:
        response = model.generate_content(user_prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Sorry, I encountered an error while processing your request. Please try again later. (Error: {e})"

    return reply, topics
