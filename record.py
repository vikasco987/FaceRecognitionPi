from pymongo import MongoClient

# Connect to MongoDB server (default is localhost:27017)
client = MongoClient("mongodb://localhost:27017/")

# Use or create the database named "data"
db = client["data"]

# Use or create the collection named "record"
record_collection = db["record"]

# Sample records to insert
records = [
    {"Id": 0, "Name": "Shubham", "Folder_Name": "Shubham"},
    {"Id": 1, "Name": "Sankar", "Folder_Name": "Sankar"},
    {"Id": 2, "Name": "Apurv", "Folder_Name": "Apurv"},
    {"Id": 3, "Name": "Rahul", "Folder_Name": "Rahul"},
    {"Id": 4, "Name": "Kittu", "Folder_Name": "Kittu"},
]

# Optional: Clear existing collection for a clean slate
record_collection.delete_many({})

# Insert the records
try:
    record_collection.insert_many(records)
    print("Data inserted successfully into MongoDB")
except Exception as e:
    print("Error inserting data:", e)
