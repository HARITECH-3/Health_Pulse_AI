# NCD Health Chatbot Architecture

## System Overview

The NCD Health Chatbot is a client-server application designed to provide information about Non-Communicable Diseases (NCDs) through an interactive chat interface.

## Architecture Components

### Backend Architecture

#### 1. FastAPI Application Layer
- **Entry Point**: `app/main.py`
- **Middleware**: CORS configuration for frontend integration
- **Router Organization**: Modular routing system
  - Users (`/api/v1/users`)
  - Chat (`/api/v1/chat`)
  - Analytics (`/api/v1/analytics`)

#### 2. Data Layer
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Models**: 
  - User management
  - Conversation tracking
  - Message storage
  - Analytics data
- **Session Management**: Dependency injection for database sessions

#### 3. Business Logic Layer
- **Knowledge Base**: Structured NCD information
- **Response Generation**: Rule-based chatbot responses
- **Analytics Engine**: User interaction analysis
- **Authentication**: JWT-based user authentication

#### 4. API Layer
- **Pydantic Schemas**: Request/response validation
- **Error Handling**: HTTP exception management
- **Documentation**: Automatic OpenAPI/Swagger generation

### Database Schema

#### Users Table
```sql
- id (PK)
- email (UNIQUE)
- username (UNIQUE)
- hashed_password
- is_active
- created_at
```

#### Conversations Table
```sql
- id (PK)
- user_id (FK)
- title
- created_at
- updated_at
```

#### Messages Table
```sql
- id (PK)
- conversation_id (FK)
- content
- is_bot
- created_at
```

#### Analytics Table
```sql
- id (PK)
- user_id (FK)
- conversation_id (FK)
- message_type
- topic_category
- sentiment
- created_at
```

### Knowledge Base Structure

The knowledge base contains structured information for each NCD:

```python
{
    "disease_name": {
        "description": "General description",
        "symptoms": ["symptom1", "symptom2", ...],
        "prevention": ["prevention1", "prevention2", ...],
        "management": ["management1", "management2", ...]
    }
}
```

## Data Flow

### 1. User Registration/Login Flow
```
Client → FastAPI → Database → JWT Token → Client
```

### 2. Chat Flow
```
Client → FastAPI → Response Engine → Knowledge Base → Bot Response → Database → Client
```

### 3. Analytics Flow
```
User Interactions → FastAPI → Analytics Engine → Database → Analytics API → Client
```

## Security Considerations

### Authentication
- JWT tokens for user authentication
- Password hashing using bcrypt
- Token expiration management

### Data Protection
- Input validation using Pydantic schemas
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for frontend access

### Privacy
- User data isolation
- Optional analytics opt-out
- Secure password storage

## Technology Stack

### Backend Technologies
- **FastAPI**: Modern web framework for APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server
- **JWT**: JSON Web Tokens for authentication
- **Passlib**: Password hashing

### Database
- **SQLite**: Default lightweight database
- **Configurable**: Easy migration to PostgreSQL/MySQL

### Development Tools
- **Python**: Programming language
- **pip**: Package management
- **Git**: Version control

## API Design Principles

### RESTful Design
- Resource-based URLs
- HTTP method semantics
- Consistent response formats
- Proper HTTP status codes

### Error Handling
- Structured error responses
- Appropriate HTTP status codes
- User-friendly error messages

### Documentation
- Auto-generated OpenAPI specs
- Interactive API documentation
- Clear endpoint descriptions

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Load balancer ready

### Performance Optimization
- Database indexing
- Query optimization
- Response caching strategies

### Monitoring
- Analytics endpoints for usage tracking
- Health check endpoints
- Error logging

## Future Architecture Enhancements

### Microservices Migration
- Separate user service
- Dedicated chat service
- Analytics service
- Knowledge base service

### AI/ML Integration
- Natural Language Processing
- Sentiment analysis
- Intent recognition
- Personalized responses

### External Integrations
- Health data APIs
- Wearable device integration
- Electronic health records
- Telemedicine platforms

### Real-time Features
- WebSocket support for real-time chat
- Live notifications
- Multi-user conversations

## Deployment Architecture

### Development Environment
- Local SQLite database
- Development server configuration
- Hot reloading support

### Production Environment
- Container-based deployment (Docker)
- Production database (PostgreSQL)
- Load balancer configuration
- SSL/TLS encryption
- Environment variable management

## Monitoring and Logging

### Application Monitoring
- API response times
- Error rates
- User activity metrics
- System resource usage

### Logging Strategy
- Structured logging format
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Log rotation and retention
- Security event logging

This architecture provides a solid foundation for the NCD Health Chatbot while allowing for future enhancements and scalability improvements.
