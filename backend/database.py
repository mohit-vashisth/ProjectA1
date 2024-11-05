from pymongo import MongoClient
from datetime import datetime

def get_database():
    # connecting to mongodb
    client = MongoClient("mongodb://3Rminds:27017/")
    db = client["3Rminds_db"]
    return db
