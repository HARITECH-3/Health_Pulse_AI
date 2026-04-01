from fastapi import APIRouter, Depends
from typing import Dict, Any
from collections import Counter
from pymongo.database import Database

from ..db import get_db

router = APIRouter()

@router.get("/health-trends")
def health_trends(db: Database = Depends(get_db)):
    msgs = list(db.messages.find({"sender": "bot"}))
    topics = []
    for m in msgs:
        t_str = m.get("topics", "")
        if t_str:
            topics.extend(t.strip() for t in t_str.split(",") if t.strip())
    counts = Counter(topics)
    return {
        "total_responses": len(msgs),
        "topic_counts": counts,
    }

@router.get("/overview")
async def get_analytics_overview(db: Database = Depends(get_db)):
    total_conversations = db.conversations.count_documents({})
    total_messages = db.messages.count_documents({})
    user_messages = db.messages.count_documents({"sender": "user"})
    bot_messages = db.messages.count_documents({"sender": "bot"})
    total_users = db.users.count_documents({})
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "user_messages": user_messages,
        "bot_messages": bot_messages,
        "total_users": total_users,
        "average_messages_per_conversation": total_messages / max(total_conversations, 1)
    }

@router.get("/users")
async def get_user_analytics(db: Database = Depends(get_db)):
    total_users = db.users.count_documents({})
    smokers = db.users.count_documents({"is_smoker": True})
    hypertension = db.users.count_documents({"has_hypertension": True})
    diabetes = db.users.count_documents({"has_diabetes": True})
    
    return {
        "total_users": total_users,
        "smokers": smokers,
        "has_hypertension": hypertension,
        "has_diabetes": diabetes,
        "smoker_percentage": (smokers / max(total_users, 1)) * 100,
        "hypertension_percentage": (hypertension / max(total_users, 1)) * 100,
        "diabetes_percentage": (diabetes / max(total_users, 1)) * 100
    }

@router.get("/conversations")
async def get_conversation_analytics(db: Database = Depends(get_db)):
    # Average conversation length using aggregation
    pipeline = [
        {"$group": {"_id": "$conversation_id", "count": {"$sum": 1}}}
    ]
    conv_counts = list(db.messages.aggregate(pipeline))
    if conv_counts:
        avg_length = sum(c["count"] for c in conv_counts) / len(conv_counts)
    else:
        avg_length = 0
    
    # Most recent conversations
    recent_conversations = list(db.conversations.find().sort("created_at", -1).limit(5))
    
    formatted_recent = []
    for conv in recent_conversations:
        msg_count = db.messages.count_documents({"conversation_id": str(conv["_id"])})
        formatted_recent.append({
            "id": str(conv["_id"]),
            "user_id": str(conv["user_id"]),
            "created_at": conv["created_at"],
            "message_count": msg_count
        })
        
    return {
        "average_conversation_length": avg_length,
        "recent_conversations": formatted_recent
    }
