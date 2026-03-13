from db.mongo import session_collection
from adaptive.next_question import get_question
from adaptive.ability import update_ability
from analysis.study_plan import generate_plan


user = input("Enter user name: ")

session = session_collection.find_one({"user_id": user})

if not session:
    print("User not found")
    exit()


ability = session["ability"]


for i in range(5):

    q = get_question(ability)

    print("\nQuestion:", q["question"])
    print("Options:", q["options"])

    ans = input("Your answer: ")

    correct = ans == q["correct_answer"]

    if correct:
        result = 1
        print("Correct")
    else:
        result = 0
        print("Wrong")

    difficulty = q["difficulty"]

    ability = update_ability(ability, result, difficulty)

    session_collection.update_one(
        {"user_id": user},
        {
            "$set": {"ability": ability},
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

    print("New ability:", ability)


print("\nTest finished")


# ✅ find weak topics
session = session_collection.find_one({"user_id": user})

answers = session["answers"]

weak_topics = []

for a in answers:
    if a["correct"] == False:
        weak_topics.append(a["topic"])

session_collection.update_one(
    {"user_id": user},
    {"$set": {"weak_topics": weak_topics}}
)


# ✅ AI plan
generate_plan(user)