# test_mongodb.py
import pymongo

# MongoDB connection parameters
mongo_host = "mongodb://localhost:27017/"
mongo_db = "test_db"
mongo_collection = "test_collection"

# Function to test MongoDB
def test_mongodb():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_host)
        db = client[mongo_db]
        collection = db[mongo_collection]

        # Insert a document
        # document = {"test_key": "test_value"}
        # collection.insert_one(document)

        # Read the inserted document
        result = collection.find_one({"test_key": "test_value"})
        print("Document retrieved:", result)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_mongodb()
