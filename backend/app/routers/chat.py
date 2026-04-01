from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId

from ..db import get_db
from ..rag_engine import build_answer
from app.schemas import ChatRequest, ChatResponse
from pymongo.database import Database

router = APIRouter()

def get_or_create_conversation(db: Database, user_id: str, conv_id: str | None, first_message: str):
    if conv_id:
        try:
            conv = db.conversations.find_one({"_id": ObjectId(conv_id), "user_id": user_id})
            if conv:
                return conv
        except Exception:
            pass
            
    # Create new
    conv_doc = {
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "title": first_message[:50] + "..." if len(first_message) > 50 else first_message
    }
    result = db.conversations.insert_one(conv_doc)
    conv_doc["_id"] = result.inserted_id
    return conv_doc

@router.post("/send", response_model=ChatResponse)
def send_message(payload: ChatRequest, db: Database = Depends(get_db)):
    # Check if user exists
    user = None
    try:
        user = db.users.find_one({"_id": ObjectId(payload.user_id)})
    except Exception:
        # Fallback if the user_id is the fake string from the old frontend
        user = db.users.find_one({"legacy_id": payload.user_id})
        
    if not user:
        # Create a fallback anonymous user if they bypass login (useful for testing)
        user_doc = {
            "name": f"Demo User",
            "legacy_id": payload.user_id,
            "created_at": datetime.utcnow()
        }
        result = db.users.insert_one(user_doc)
        user = user_doc
        payload.user_id = str(result.inserted_id)
    else:
        payload.user_id = str(user["_id"])

    # Conversation tracking
    conv = get_or_create_conversation(db, payload.user_id, payload.conversation_id, payload.message)
    conv_id_str = str(conv["_id"])

    # Save user message
    user_msg = {
        "conversation_id": conv_id_str,
        "sender": "user",
        "text": payload.message,
        "created_at": datetime.utcnow()
    }
    db.messages.insert_one(user_msg)

    # Personalization contexts
    user_profile = {
        "is_smoker": user.get("is_smoker", False),
        "has_hypertension": user.get("has_hypertension", False),
        "has_diabetes": user.get("has_diabetes", False),
    }

    # History builder
    last_msgs_cursor = db.messages.find({"conversation_id": conv_id_str}).sort("created_at", -1).limit(5)
    last_msgs = list(last_msgs_cursor)
    history_texts = [m["text"] for m in reversed(last_msgs) if "text" in m]

    # Generate Response
    reply_text, topics = build_answer(
        user_profile=user_profile,
        query=payload.message,
        history=history_texts,
    )

    # Save bot reply
    bot_msg = {
        "conversation_id": conv_id_str,
        "sender": "bot",
        "text": reply_text,
        "topics": ",".join(topics),
        "created_at": datetime.utcnow()
    }
    bot_result = db.messages.insert_one(bot_msg)

    return ChatResponse(
        message=reply_text,
        conversation_id=conv_id_str,
        message_id=str(bot_result.inserted_id)
    )
