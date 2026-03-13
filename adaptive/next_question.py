from db.mongo import questions_collection


def get_question(ability):

    q = questions_collection.find_one(
        {"difficulty": {"$gte": ability}},
        sort=[("difficulty", 1)]
    )

    return q