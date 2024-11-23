from .conexao_mongo import get_db

def insert_message(collection_name, message_data):
    db = get_db()
    collection = db[collection_name]
    result = collection.insert_one(message_data)
    return result.inserted_id

def get_all_messages(collection_name):
    db = get_db()
    collection = db[collection_name]
    return list(collection.find())
