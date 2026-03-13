<<<<<<< HEAD
# ability_testing_training
AI-powered Adaptive Testing System: Dynamically selects questions based on user performance, generates personalized study plans, and tracks answers via REST API. Built with Python &amp; FastAPI, it uses AI tools for development while keeping API keys secure via environment variables.
=======
# Adaptive Testing System

An intelligent adaptive testing platform built with FastAPI, MongoDB, and Groq AI that personalizes learning experiences through dynamic question selection and AI-generated study plans.

## Features

- **Adaptive Question Selection**: Uses ability estimation algorithms to select questions based on student performance
- **Real-time Ability Tracking**: Continuously updates student ability scores using Item Response Theory
- **Weak Topic Identification**: Automatically detects and analyzes weak areas in student knowledge
- **AI-Powered Study Plans**: Generates personalized study schedules using Groq AI based on ability level and weak topics
- **Session Management**: Supports multiple test attempts with progress comparison
- **RESTful API**: Clean FastAPI endpoints for easy integration

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: Groq API (Llama 3.1 model)
- **Environment**: Python virtual environment with dotenv for secrets

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd prroject_C17
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi pymongo groq python-dotenv uvicorn
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual MongoDB URL and Groq API key
   ```

5. **Seed the database** (optional)
   ```bash
   python seed_question.py
   ```

## Usage

1. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

2. **API Endpoints**

   - `GET /check_user/{user}` - Check if user exists
   - `POST /create_user/{user}` - Create new user session
   - `GET /question/{user}` - Get next adaptive question
   - `POST /answer` - Submit answer and update ability
   - `GET /plan/{user}` - Generate personalized study plan (requires 10+ questions)
   - `POST /refresh/{user}` - Reset session for retake
   - `GET /session/{user}` - Get session information

## Project Structure

```
├── adaptive/
│   ├── ability.py          # Ability estimation logic
│   └── next_question.py    # Question selection algorithm
├── analysis/
│   ├── study_plan.py       # AI study plan generation
│   └── weak_topic.py       # Weak topic identification
├── db/
│   └── mongo.py            # Database connection and collections
├── config.py               # Configuration and environment variables
├── main.py                 # FastAPI application
├── seed_question.py        # Database seeding script
├── test_engine.py          # Testing utilities
└── ui.py                   # User interface components
```

## Configuration

The application uses environment variables for sensitive data:

- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name (default: adaptive_test)
- `GROQ_API_KEY`: API key for Groq AI service

Copy `.env.example` to `.env` and fill in your values.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.
>>>>>>> 294a81c (First Python project commit)
