from .conexao_mongo import obter_conexao_mongo


def insert_message(collection_name, message_data):
    db = obter_conexao_mongo()
    collection = db[collection_name]
    result = collection.insert_one(message_data)
    return result.inserted_id


def get_all_messages(collection_name):
    db = obter_conexao_mongo()
    collection = db[collection_name]
    return list(collection.find())
