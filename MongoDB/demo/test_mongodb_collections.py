# test_mongodb.py
import pymongo

# MongoDB connection parameters
mongo_host = "mongodb://10.141.10.72:32717/"
mongo_db = "data_db"
mongo_collection = "telemetry"

# Function to test MongoDB


def test_mongodb():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_host)
        db = client[mongo_db]
        collection = db[mongo_collection]

        result = collection.find({})
        documents = list(result)
        print("Documents retrieved:", documents)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    test_mongodb()
