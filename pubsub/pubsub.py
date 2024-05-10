from pymongo import MongoClient
import datetime

def add_to_database(document, db_addr, db_base, db_collection):
    client = MongoClient(db_addr)
    database = client[db_base]
    collection = database[db_collection]
    collection.insert_one(document)

def download_from_database(key, db_addr, db_base, db_collection): 
    client = MongoClient(db_addr)
    database = client[db_base]
    collection = database[db_collection]
    return collection.find_one(key)

def prepare_for_database(data, user):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    document = {
    "date": current_time,
    "author": user,
    
    }
    return document

print(prepare_for_database(0, "Mikołaj"))