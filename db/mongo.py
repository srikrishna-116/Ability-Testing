from pymongo import MongoClient
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)

db = client[DB_NAME]

questions_collection = db["questions"]
session_collection = db["usersession"]