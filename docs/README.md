# NCD Health Chatbot

A comprehensive chatbot system for providing information about Non-Communicable Diseases (NCDs).

## Overview

This project consists of a FastAPI backend with a built-in knowledge base for NCDs including:
- Diabetes
- Cardiovascular diseases
- Cancer
- Chronic respiratory diseases

## Features

### Backend
- **User Management**: Registration and authentication system
- **Chat System**: Real-time conversation with AI-powered responses
- **Knowledge Base**: Structured information about NCDs
- **Analytics**: Track user interactions and conversation patterns
- **RESTful API**: Well-documented endpoints for frontend integration

### API Endpoints

#### Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user info

#### Chat
- `POST /api/v1/chat/send` - Send message to chatbot
- `GET /api/v1/chat/conversations` - Get user conversations
- `GET /api/v1/chat/conversations/{id}/messages` - Get conversation messages

#### Analytics
- `GET /api/v1/analytics/overview` - Get usage overview
- `GET /api/v1/analytics/topics` - Get topic analytics
- `GET /api/v1/analytics/conversations/stats` - Get conversation statistics
- `GET /api/v1/analytics/health-trends` - Get health trend analysis

## Project Structure

```
ncd_health_chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── db.py                # Database connection and session
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── knowledge_base.py    # NCD knowledge base
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── users.py         # User management endpoints
│   │       ├── chat.py          # Chat functionality
│   │       └── analytics.py     # Analytics endpoints
│   └── requirements.txt         # Python dependencies
├── frontend/                    # Frontend implementation (placeholder)
├── docs/
│   ├── README.md               # This file
│   └── architecture.md         # Detailed architecture documentation
├── data/
│   ├── sample_ncd_content.md   # Sample NCD content
│   └── sample_conversations.json # Sample conversation data
└── .gitignore                 # Git ignore file
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   cd backend
   python -m app.main
   ```
   or using uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`
3. API documentation available at `http://localhost:8000/docs`

### Database

The application uses SQLite by default. The database file will be created automatically on first run.

## Development

### Adding New Diseases

To add new diseases to the knowledge base, update the `ncd_data` dictionary in `knowledge_base.py`.

### Extending Analytics

Add new analytics endpoints in `app/routers/analytics.py` following the existing patterns.

### Frontend Integration

The frontend can communicate with the backend using the documented API endpoints. Authentication tokens should be included in the Authorization header for protected routes.

## Future Enhancements

- Machine learning integration for better response generation
- Integration with external health APIs
- Multi-language support
- Mobile app development
- Real-time notifications
- Integration with wearable devices
