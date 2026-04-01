# NCD Health Chatbot

A comprehensive chatbot system for providing information about Non-Communicable Diseases (NCDs) including diabetes, cardiovascular diseases, cancer, and chronic respiratory diseases.

## Features

- **Interactive Chat Interface**: Natural language processing for health-related queries
- **Disease Information**: Detailed knowledge base for various NCDs
- **User Authentication**: Secure user accounts and session management
- **Conversation History**: Track and review past interactions
- **Analytics Dashboard**: Insights into user interactions and health trends

## Project Structure

```
ncd_health_chatbot/
├── backend/               # FastAPI backend application
│   ├── app/              # Main application package
│   └── requirements.txt  # Python dependencies
├── frontend/             # Frontend application (to be implemented)
├── data/                 # Sample data and content
└── docs/                 # Documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite (for development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ncd_health_chatbot.git
   cd ncd_health_chatbot
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`
3. Access the interactive API documentation at `http://localhost:8000/docs`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Development

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./ncd_chatbot.db
```

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- Mypy for type checking

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)
