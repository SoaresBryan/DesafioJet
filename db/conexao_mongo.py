import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def obter_conexao_mongo():
    """
    Retorna a conexão com o banco de dados MongoDB.

    :return: Objeto de banco de dados MongoDB.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client["chatbot"]
        return db
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        raise
