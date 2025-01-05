from datetime import timedelta
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from utils.converters import serialize_sqlalchemy_obj
from models.responses import BaseResponse
from models.responses.token_response import TokenResponse
from models.requests import CreateUserRequest
from dependencies import db_dependency, form_data_dependency
import services.user_service as user_service
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseResponse)
async def create_user(db: db_dependency,
                      user: user_service.user_dependency,
                      create_user_request: CreateUserRequest):
    try:
        if user.get('user_role') != 'admin':
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BaseResponse(
                    status=401,
                    message="Unauthorized",
                    data={}
                ).model_dump()
            )

        created_user = await user_service.create_user(create_user_request, db)

        if not created_user:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BaseResponse(
                    status=500,
                    message="Could not create user",
                    data={}
                ).model_dump()
            )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=BaseResponse(
                status=201,
                message="User created successfully",
                data=jsonable_encoder(serialize_sqlalchemy_obj(created_user))
            ).model_dump()
        )
    except IntegrityError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponse(
                status=400,
                message=f"Could not create user - {e.orig}",
                data={}
            ).model_dump()
        )
    
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BaseResponse(
                status=501,
                message="Internal Server Error",
                data={}
            ).model_dump()
        )

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: form_data_dependency,
                                 db: db_dependency):
    try:
        user = user_service.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BaseResponse(
                    status=401,
                    message="Unauthorized",
                    data={}
                ).model_dump()
            )

        token = user_service.create_access_token(user.username, user.id, user.role, timedelta(hours=1))

        return TokenResponse(access_token=token, token_type='bearer')
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BaseResponse(
                status=500,
                message="Internal Server Error",
                data={}
            ).model_dump()
        )