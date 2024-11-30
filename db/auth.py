from fastapi import HTTPException, Header
import logging


async def get_user_id(x_user_id: str = Header(...)):
    """
    Obtém o ID do usuário a partir do header 'X-User-ID'.

    :param x_user_id: O ID do usuário passado no header 'X-User-ID'.
    :return: O ID do usuário.
    :raises HTTPException: Se o header 'X-User-ID' estiver ausente.
    """
    if not x_user_id:
        logging.error("Header 'X-User-ID' ausente. Usuário: Desconhecido")
        raise HTTPException(status_code=400, detail="X-User-ID header missing")
    return x_user_id
