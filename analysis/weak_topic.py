from db.mongo import session_collection


def find_weak_topics(user):

    session = session_collection.find_one({"user_id": user})

    answers = session["answers"]

    topic_wrong = {}

    for a in answers:

        if not a["correct"]:

            t = a["topic"]

            if t not in topic_wrong:
                topic_wrong[t] = 0

            topic_wrong[t] += 1

    weak = list(topic_wrong.keys())

    session_collection.update_one(
        {"user_id": user},
        {"$set": {"weak_topics": weak}}
    )

    return weak