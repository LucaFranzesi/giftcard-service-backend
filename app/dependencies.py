from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.encryption import oauth2_bearer
from db.database import get_db

form_data_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
token_dependency = Annotated[str, Depends(oauth2_bearer)]
db_dependency = Annotated[Session, Depends(get_db)]