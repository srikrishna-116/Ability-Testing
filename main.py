import logging

from fastapi import FastAPI
from db.mongo import (
    questions_collection,
    session_collection
)

from adaptive.next_question import get_question
from adaptive.ability import update_ability
from analysis.study_plan import generate_plan
from analysis.weak_topic import find_weak_topics

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# -----------------------------
# CHECK USER
# -----------------------------
@app.get("/check_user/{user}")
def check_user(user: str):
    session = session_collection.find_one({"user_id": user})
    exists = bool(session)
    logger.info("check_user: %s exists=%s", user, exists)
    return {"exists": exists}


@app.get("/session/{user}")
def session_info(user: str):
    session = session_collection.find_one({"user_id": user})
    if not session:
        return {"exists": False}

    answered = len(session.get("answers", []))
    prev_answers = len(session.get("previous_answers", []))

    return {
        "exists": True,
        "answered": answered,
        "ability": session.get("ability", 0.5),
        "weak_topics": session.get("weak_topics", []),
        "has_previous": prev_answers > 0,
        "attempts": session.get("attempts", 1),
    }

# -----------------------------
# CREATE USER
# -----------------------------
@app.post("/create_user/{user}")
def create_user(user: str):
    session = session_collection.find_one({"user_id": user})
    if session:
        logger.info("create_user: %s already exists", user)
        return {"msg": "user exists"}

    new_session = {
        "user_id": user,
        "ability": 0.5,
        "answers": [],
        "weak_topics": [],
        # For retakes: keep the previous test results for comparison
        "previous_answers": [],
        "previous_weak_topics": [],
        "previous_ability": 0.5,
        "attempts": 1,
    }
    session_collection.insert_one(new_session)
    logger.info("create_user: %s created", user)
    return {"msg": "user created"}

# -----------------------------
# GET QUESTION
# -----------------------------
@app.get("/question/{user}")
def get_question(user: str):
    session = session_collection.find_one({"user_id": user})
    if not session:
        logger.warning("get_question: user not found (%s)", user)
        return {"error": "user not found"}

    answered = [a["question"] for a in session.get("answers", [])]
    q = questions_collection.find_one({"question": {"$nin": answered}})
    if not q:
        logger.info("get_question: no new question for user %s", user)
        return {"error": "no new question available"}

    # Save last question in session
    session_collection.update_one(
        {"user_id": user},
        {"$set": {"last_question": q["question"]}}
    )

    logger.info("get_question: served question for user %s", user)
    return {
        "question": q["question"],
        "options": q["options"]
    }
 
# -----------------------------
# ANSWER
# -----------------------------
@app.post("/answer")
def answer(user: str, ans: str):
    session = session_collection.find_one({"user_id": user})
    if not session:
        logger.warning("answer: user not found (%s)", user)
        return {"error": "user not found"}

    ability = session["ability"]
    last_q_text = session.get("last_question")

    if not last_q_text:
        logger.warning("answer: no question asked yet for user %s", user)
        return {"error": "no question asked yet"}

    q = questions_collection.find_one({"question": last_q_text})
    if not q or "correct_answer" not in q:
        logger.error("answer: invalid question data for user %s, question=%s", user, last_q_text)
        return {"error": "invalid question data"}

    correct = ans == q["correct_answer"]
    result = 1 if correct else 0
    difficulty = q["difficulty"]

    new_ability = update_ability(ability, result, difficulty)

    session_collection.update_one(
        {"user_id": user},
        {
            "$set": {"ability": new_ability},
            "$push": {
                "answers": {
                    "question": q["question"],
                    "topic": q["topic"],
                    "difficulty": difficulty,
                    "correct": correct
                }
            }
        }
    )

    logger.info("answer: user=%s question=%s correct=%s new_ability=%.3f", user, last_q_text, correct, new_ability)
    return {"correct": correct, "ability": new_ability}

# -----------------------------
# STUDY PLAN
# -----------------------------
# STUDY PLAN
# -----------------------------
@app.get("/plan/{user}")
def plan(user: str):
    session = session_collection.find_one({"user_id": user})
    if not session:
        logger.warning("plan: user not found (%s)", user)
        return {"error": "user not found"}

    # Check if at least 10 questions have been answered
    answered_questions = len(session.get("answers", []))

    if answered_questions < 10:
        logger.info("plan: not enough answers for user %s (%d answered)", user, answered_questions)
        return {"msg": "Complete at least 10 questions to see your study plan."}

    # Compute weak topics for the current attempt (updates session weak_topics)
    weak = find_weak_topics(user)
    study_plan = generate_plan(user)

    # Compare this attempt to the previous attempt (if any)
    prev_answers = session.get("previous_answers", [])
    prev_ability = session.get("previous_ability", 0.5)
    prev_weak = session.get("previous_weak_topics", [])

    current_answers = session.get("answers", [])
    current_ability = session.get("ability", 0.5)

    def correct_count(ans_list):
        return sum(1 for a in ans_list if a.get("correct"))

    comparison = {
        "prev_correct": correct_count(prev_answers),
        "new_correct": correct_count(current_answers),
        "prev_ability": prev_ability,
        "new_ability": current_ability,
        "prev_weak_topics": prev_weak,
        "new_weak_topics": weak,
    }

    logger.info("plan: generated plan for user %s (answered=%d)", user, answered_questions)
    return {
        "plan": study_plan,
        "weak_topics": weak,
        "answers": current_answers,
        "comparison": comparison,
    }
# -----------------------------
# REFRESH SESSION
# -----------------------------
@app.post("/refresh/{user}")
def refresh(user: str):
    session = session_collection.find_one({"user_id": user})

    if session:
        # Save current test as previous test
        session_collection.update_one(
            {"user_id": user},
            {
                "$set": {
                    "previous_answers": session.get("answers", []),
                    "previous_ability": session.get("ability", 0.5),
                    "previous_weak_topics": session.get("weak_topics", []),
                    "ability": 0.5,
                    "answers": [],
                    "weak_topics": [],
                    "last_question": None,
                },
                "$inc": {"attempts": 1}
            },
        )
        logger.info("refresh: refreshed session for user %s", user)
    else:
        # Create new session if missing
        new_session = {
            "user_id": user,
            "ability": 0.5,
            "answers": [],
            "weak_topics": [],
            "previous_answers": [],
            "previous_weak_topics": [],
            "previous_ability": 0.5,
        }
        session_collection.insert_one(new_session)
        logger.info("refresh: created session for new user %s", user)

    return {"msg": "session refreshed"}


if __name__ == "__main__":
    """Run both the FastAPI server and the Streamlit UI when executing this file directly.

    Usage:
        python main.py

    This will start:
      - FastAPI app on http://localhost:8000
      - Streamlit UI on http://localhost:8501
    """

    import subprocess
    import sys

    # Run uvicorn and streamlit in parallel subprocesses
    procs = []
    try:
        procs.append(subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]))
        procs.append(subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ui.py", "--server.port", "8501"]))

        # Wait for both processes to exit (they run until interrupted)
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        # Clean up on Ctrl+C
        for p in procs:
            if p.poll() is None:
                p.terminate()
        for p in procs:
            p.wait()
