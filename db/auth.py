from fastapi import Depends, HTTPException, Header

async def get_user_id(x_user_id: str = Header(...)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header missing")
    return x_user_id
