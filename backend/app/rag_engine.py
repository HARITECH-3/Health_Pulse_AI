from pathlib import Path
from typing import List, Tuple
from sentence_transformers import SentenceTransformer, util

# Model will be loaded lazily to prevent blocking startup

class KnowledgeChunk:
    def __init__(self, text: str, topic: str):
        self.text = text
        self.topic = topic

# --- load and chunk documents ---
def load_knowledge(base_path: str = "../data") -> List[KnowledgeChunk]:
    chunks: List[KnowledgeChunk] = []
    folder = Path(base_path)
    for path in folder.glob("*.md"):
        topic = path.stem  # filename without extension
        text = path.read_text(encoding="utf-8")
        # simple splitting by paragraphs
        for para in text.split("\n\n"):
            para = para.strip()
            if len(para) > 80:  # ignore very short
                chunks.append(KnowledgeChunk(para, topic))
    return chunks

knowledge_chunks = load_knowledge()
_initialized = False
model = None
knowledge_embeddings = None

def _init_rag():
    global _initialized, model, knowledge_embeddings
    if not _initialized:
        print("Lazy loading SentenceTransformer model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        if knowledge_chunks:
            knowledge_texts = [c.text for c in knowledge_chunks]
            knowledge_embeddings = model.encode(knowledge_texts, convert_to_tensor=True)
        _initialized = True

def retrieve_relevant(query: str, top_k: int = 3) -> List[KnowledgeChunk]:
    if not knowledge_chunks:
        return []
        
    _init_rag()
    
    query_emb = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, knowledge_embeddings, top_k=top_k)[0]
    return [knowledge_chunks[h["corpus_id"]] for h in hits]

def build_answer(
    user_profile: dict,
    query: str,
    history: List[str],
) -> Tuple[str, List[str]]:
    """
    Returns (reply_text, topics)
    Uses the retrieved chunks and google.generativeai to form a response based on the Pulse Health AI system prompt.
    """
    retrieved = retrieve_relevant(query)
    topics = list({c.topic for c in retrieved})

    # Personalized intro
    intro_parts = []
    if user_profile.get("is_smoker"):
        intro_parts.append(
            "Note: Because you smoke, your risk of heart and lung disease is higher."
        )
    if user_profile.get("has_hypertension"):
        intro_parts.append(
            "Note: You mentioned high blood pressure, so controlling salt and stress is important."
        )
    if user_profile.get("has_diabetes"):
        intro_parts.append(
            "Note: With diabetes, healthy diet and regular follow-up visits are very important."
        )

    # Safety rule: emergencies
    red_flags = ["chest pain", "severe headache", "difficulty breathing"]
    if any(flag in query.lower() for flag in red_flags):
        emergency = (
            "You mentioned a serious symptom. Please go to the nearest clinic "
            "or emergency service immediately. Do not rely on chatbot advice only. "
        )
        return emergency, ["emergency"]

    # Combine retrieved knowledge context
    context_knowledge = ""
    if retrieved:
        context_knowledge = "\n\nRelevant Excerpts from Knowledge Base:\n" + "\n".join(c.text for c in retrieved)

    # Build the conversation payload for the LLM
    from app.config import settings
    import google.generativeai as genai
    from .prompts import PULSE_HEALTH_AI_PROMPT

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return (
            "[SYSTEM NOTIFICATION: The AI backend GEMINI_API_KEY is not configured. "
            "Please check the .env file. Returning retrieved context.]\n\n"
            + "".join(intro_parts) + "\n\n" + (context_knowledge if retrieved else "No context found.")
        ), topics

    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash which is standard and fast
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=PULSE_HEALTH_AI_PROMPT
    )

    # Constructing user prompt with context and history
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

# Force trigger backend hot-reload
