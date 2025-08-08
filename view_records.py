from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the database and collection
db = client["data"]
record_collection = db["record"]

# Fetch all documents
records = record_collection.find()

# Print them
for record in records:
    print(record)
