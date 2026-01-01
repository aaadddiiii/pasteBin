# db/mongo.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os, config

load_dotenv()
config.MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
pastes = db[config.MONGO_COLLECTION]
