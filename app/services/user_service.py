from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from utils.encryption import bcrypt_context
from configurations import config
from dependencies import token_dependency, db_dependency
from models.database.user import User
from jose import jwt, JWTError


async def get_current_user(token: token_dependency):
    try:
        payload = jwt.decode(token, config.BCRYPT_SECRET_KEY, algorithms=[config.BCRYPT_ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

user_dependency = Annotated[dict, Depends(get_current_user)]


async def create_user(create_user_request, db):
    
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

    return create_user_model

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, config.BCRYPT_SECRET_KEY, algorithm=config.BCRYPT_ALGORITHM)