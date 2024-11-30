from .conexao_mongo import obter_conexao_mongo
import logging


def insert_message(collection_name, message_data):
    """
    Insere uma mensagem em uma coleção MongoDB especificada.

    :param collection_name: Nome da coleção MongoDB.
    :param message_data: Dados a serem inseridos.
    :return: ID do documento inserido.
    """
    try:
        db = obter_conexao_mongo()
        collection = db[collection_name]
        result = collection.insert_one(message_data)
        return result.inserted_id
    except Exception as e:
        logging.error(f"Erro ao inserir mensagem em {collection_name}: {e}")
        raise


def get_all_messages(collection_name):
    """
    Recupera todas as mensagens de uma coleção MongoDB especificada.

    :param collection_name: Nome da coleção MongoDB.
    :return: Lista de mensagens.
    """
    try:
        db = obter_conexao_mongo()
        collection = db[collection_name]
        return list(collection.find())
    except Exception as e:
        logging.error(f"Erro ao recuperar mensagens de {collection_name}: {e}")
        raise


def salvar_interacao(user_id: str, prompt: str, resposta: str):
    """
    Salva a interação (prompt e resposta) no MongoDB.

    :param user_id: ID do usuário.
    :param prompt: Pergunta do usuário.
    :param resposta: Resposta da IA.
    """
    try:
        db = obter_conexao_mongo()
        colecao = db["interacoes"]
        colecao.insert_one({
            "user_id": user_id,
            "prompt": prompt,
            "resposta": resposta
        })
    except Exception as e:
        logging.error(f"Erro ao salvar interação para o usuário {user_id}: {e}")
        raise


def recuperar_interacoes(user_id: str):
    """
    Recupera as interações anteriores de um usuário.

    :param user_id: ID do usuário.
    :return: Lista de interações (prompt e resposta).
    """
    try:
        db = obter_conexao_mongo()
        colecao = db["interacoes"]
        interacoes = colecao.find({"user_id": user_id})
        return [
            {"prompt": i["prompt"], "resposta": i["resposta"]}
            for i in interacoes
        ]
    except Exception as e:
        logging.error(f"Erro ao recuperar interações para o usuário {user_id}: {e}")
        raise
