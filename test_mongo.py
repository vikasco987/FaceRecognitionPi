from pymongo import MongoClient

# For local MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["attendanceDB"]
collection = db["attendances"]

# Insert a test document
collection.insert_one({"name": "krishna", "status": "Present"})

# Read it back
for doc in collection.find():
    print(doc)
