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

---

## Quick Start

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
   pip install -r requirements.txt
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

6. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

---

## API Endpoints

- `GET /check_user/{user}` - Check if user exists
- `POST /create_user/{user}` - Create new user session
- `GET /question/{user}` - Get next adaptive question
- `POST /answer` - Submit answer and update ability
- `GET /plan/{user}` - Generate personalized study plan (requires 10+ questions)
- `POST /refresh/{user}` - Reset session for retake
- `GET /session/{user}` - Get session information

---

## Logging & Debugging

This project uses FastAPI / Uvicorn logging by default. To increase verbosity for debugging, run the server with a higher log level:

```bash
uvicorn main:app --reload --log-level debug
```

### Where to look for runtime issues

- **MongoDB connectivity**: Verify `MONGO_URL` in `.env` and that MongoDB is running.
- **Missing environment variables**: Ensure `GROQ_API_KEY` is set if you want to generate study plans.
- **Study plan generation**: Requires at least 10 submitted answers; otherwise the endpoint returns a message asking you to complete more questions.

---

## Common Issues & Troubleshooting

### 1) Server fails to start

- Make sure your virtual environment is activated.
- Confirm dependencies are installed (`pip install -r requirements.txt`).
- Check the console for stack traces, especially for MongoDB connection errors.

### 2) API returns `user not found`

- Create a user first using `POST /create_user/{user}`.
- Ensure the `user` path parameter matches exactly (case-sensitive).

### 3) Study plan not generating

- The `/plan/{user}` endpoint requires at least **10 answered questions**.
- If you see "Complete at least 10 questions to see your study plan", continue answering questions via `/question/{user}` + `/answer`.

---

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

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is open source. Please check the license file for details.
