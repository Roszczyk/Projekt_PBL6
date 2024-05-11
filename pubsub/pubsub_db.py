from pymongo import MongoClient
import datetime
import json
from collections import defaultdict

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

def prepare_document(data, hive):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    document = {
    "date": current_time,
    "hive": hive,   
    }
    if type(data)==dict and len(data)>0:
        document.update(data)
    return document

def parse_received_date(date):
    date = date.split("T")
    time = date[1]
    date = date[0]
    time = time.split(".")[0]
    return f"{date} {time}"


def payload_format(payload: str):
    document = dict()
    payload = json.loads(payload)

    default_dict = defaultdict(lambda: None, payload['decoded_payload'])

    dev_eui = payload['dev_EUI']
    timestamp = parse_received_date(payload["received_at"])
    temperature = default_dict['temperature_0']
    humidity = default_dict['relative_humidity_0']
    gps_lat = default_dict['gps_0']['latitude'] if default_dict['gps_0'] else None
    gps_lon = default_dict['gps_0']['longitude'] if default_dict['gps_0'] else None

    if default_dict['presence_0']=="0xFF":
        noise=True
        activity=True
    elif default_dict['presence_0']=="0xF0":
        noise=True
        activity=False
    elif default_dict['presence_0']=="0x0F":
        noise=False
        activity=True
    elif default_dict['presence_0']=="0x01":
        noise=False
        activity=False
    else:        
        noise=None
        activity=None

    digital_in_0 = default_dict['digital_in_0']

    digital_in_1 = default_dict['digital_in_1']
    digital_in_2 = default_dict['digital_in_2']

    document.update({"dev_EUI":dev_eui, "time":timestamp})
    if temperature != None:
        document.update({"temperature":temperature})
    if humidity != None:
        document.update({"humidity":humidity})
    if default_dict['gps_0'] != None:
        document.update({"gps_lat":gps_lat, "gps_lon":gps_lon})
    if noise != None:
        document.update({"noise":noise, "activity":activity})
    if digital_in_0 != None:
        document.update({"digital_in_0":digital_in_0})
    if digital_in_1 != None:
        document.update({"digital_in_1":digital_in_1})
    if digital_in_2 != None:
        document.update({"digital_in_2":digital_in_2})

    return document