from groq import Groq
from db.mongo import session_collection
from config import API_key

client = Groq(api_key=API_key)

def generate_plan(user):
    session = session_collection.find_one({"user_id": user})

    weak = session.get("weak_topics", [])
    ability = session.get("ability", 0.5)

    prompt = f"""
You are an AI tutor.

Student ability score: {ability}
Weak topics: {weak}

Create a personalized study plan.

Rules:
- Plan must be topic-wise
- Focus more on weak topics
- Give weekly schedule
- Give daily study time
- Give tips based on ability level
- If ability < 0.5 → beginner plan
- If ability 0.5–0.7 → medium plan
- If ability > 0.7 → advanced plan
- Include practice, revision, and mock tests

Output format:

1. Ability level
2. Weak topics analysis
3. Study schedule (day wise)
4. Topic wise plan
5. Tips to improve
6. Extra advice
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content

