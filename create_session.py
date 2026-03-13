from db.mongo import session_collection

user = input("Enter user name: ")

session = {
    "user_id": user,
    "ability": 0.2,
    "answers": [],
    "weak_topics": []
}

session_collection.insert_one(session)

print("Session created for", user)