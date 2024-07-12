import os
import json
import certifi
import time
import params
from pymongo import MongoClient

mongo_client = MongoClient(params.mongodb_conn_string, tlsCAFile=certifi.where())
result_collection = mongo_client[params.database][params.collection]

def upload_json_files(directory='Combined'):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            try:
                result_collection.insert_many(data)
            except Exception as e:
                print(f"Error uploading {filename}: {e}")

upload_json_files()