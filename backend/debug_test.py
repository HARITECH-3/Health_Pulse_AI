from app.db import SessionLocal
from app.routers.chat import send_message, ChatRequest
import traceback

db = SessionLocal()
req = ChatRequest(user_id=1, message="Hello", conversation_id=None)

try:
    res = send_message(req, db)
    print("Success:", res)
except Exception as e:
    traceback.print_exc()
