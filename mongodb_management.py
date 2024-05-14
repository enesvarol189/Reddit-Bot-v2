import os
import time
from pymongo import MongoClient

_conn_str = os.getenv('MONGODB_CONN_STR')

_client = MongoClient(_conn_str)

_db = _client.plant_clinic_bot
_collection_archived_logs = _db.archived_logs
_collection_env_variables = _db.env_variables

def get_env_variable(var_name):
    doc = _collection_env_variables.find_one()
    return doc.get(var_name) if doc else None

def get_env_variables():
    return _collection_env_variables.find_one()

env = get_env_variables()

if env is None:
    raise Exception("Environment variables could not be loaded.")

def archive_document(post_id, post_data, archived_logs):
    elapsed_time = int(time.time() - post_data["timestamp"])

    if elapsed_time >= env["data_archive_threshold"]:
        archived_document = {"post_id": post_id, **post_data}
        archived_logs.append(archived_document)
        _collection_archived_logs.insert_one(archived_document)
