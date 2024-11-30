# db/conexao_mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def obter_conexao_mongo():
    """
    Retorna a conexão com o banco de dados MongoDB.
    """
    client = MongoClient(MONGO_URI)
    db = client["chatbot"]
    return db


def salvar_interacao(user_id: str, prompt: str, resposta: str):
    """
    Salva a interação (prompt e resposta) no MongoDB.

    :param user_id: ID do usuário.
    :param prompt: Pergunta do usuário.
    :param resposta: Resposta da IA.
    """
    db = obter_conexao_mongo()
    colecao = db["interacoes"]
    colecao.insert_one({
        "user_id": user_id,
        "prompt": prompt,
        "resposta": resposta
    })


def recuperar_interacoes(user_id: str):
    """
    Recupera as interações anteriores de um usuário.

    :param user_id: ID do usuário.
    :return: Lista de interações (prompt e resposta).
    """
    db = obter_conexao_mongo()
    colecao = db["interacoes"]
    interacoes = colecao.find({"user_id": user_id})
    return [
        {"prompt": i["prompt"], "resposta": i["resposta"]}
        for i in interacoes
    ]
