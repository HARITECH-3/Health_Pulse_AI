from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    is_bot: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversation schemas
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

# Chat schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    message_id: str

# Analytics schemas
class AnalyticsBase(BaseModel):
    message_type: str
    topic_category: Optional[str] = None
    sentiment: Optional[str] = None

class AnalyticsResponse(AnalyticsBase):
    id: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class DirectResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
