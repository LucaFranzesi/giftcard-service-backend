from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from models.database import GiftCard
from models.requests import CreateGiftCardRequest, GetListPaginatedRequest
from services import gift_card_service
from utils.converters import serialize_sqlalchemy_obj
from models.responses import BaseResponse
from dependencies import db_dependency
import services.user_service as user_service
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/gift-cards',
    tags=['GiftCard']
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BaseResponse)
async def create_gift_card(db: db_dependency,
                      user: user_service.user_dependency,
                      create_gift_card_request: CreateGiftCardRequest):
    
    try:
        if user.get('user_role') != 'admin' and user.get('user_role') != 'user' :
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BaseResponse(
                    status=401,
                    message="Unauthorized",
                    data={}
                ).model_dump()
            )

        if create_gift_card_request.amount <= 0 :
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=BaseResponse(
                    status=400,
                    message=f"Could not create gift card - Amount should be positive",
                    data={}
                ).model_dump()
            )

        if create_gift_card_request.expiration != None and create_gift_card_request.expiration < datetime.now(timezone.utc) :
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=BaseResponse(
                    status=400,
                    message=f"Could not create gift card - Expiration should be in the future",
                    data={}
                ).model_dump()
            )

        created_gift_card = await gift_card_service.create_gift_card(create_gift_card_request, db)

        if not created_gift_card:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=BaseResponse(
                    status=500,
                    message="Could not create gift card",
                    data={}
                ).model_dump()
            )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=BaseResponse(
                status=201,
                message="Gift card created successfully",
                data=jsonable_encoder(serialize_sqlalchemy_obj(created_gift_card))
            ).model_dump()
        )
    except IntegrityError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponse(
                status=400,
                message=f"Could not create gift card - {e.orig}",
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
    
@router.get("/get/{code}", status_code=status.HTTP_200_OK, response_model=BaseResponse)
async def get_gift_card(db: db_dependency,
                      user: user_service.user_dependency,
                      code: str):
    
    try:
        if user.get('user_role') != 'admin' and user.get('user_role') != 'user' :
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BaseResponse(
                    status=401,
                    message="Unauthorized",
                    data={}
                ).model_dump()
            )

        gift_card = await gift_card_service.get_gift_card(code, db)

        if gift_card is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=BaseResponse(
                    status=404,
                    message="Giftcard with provived code not found",
                    data={}
                ).model_dump()
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=BaseResponse(
                status=200,
                message="Gift card retrieved successfully",
                data=jsonable_encoder(serialize_sqlalchemy_obj(gift_card))
            ).model_dump()
        )
    except IntegrityError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponse(
                status=400,
                message=f"Could not create get gift card - {e.orig}",
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
    
@router.post("/list", status_code=status.HTTP_200_OK, response_model=BaseResponse)
async def get_gift_cards(db: db_dependency,
                      user: user_service.user_dependency,
                      request: GetListPaginatedRequest):
    
    try:
        if user.get('user_role') != 'admin' and user.get('user_role') != 'user' :
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=BaseResponse(
                    status=401,
                    message="Unauthorized",
                    data={}
                ).model_dump()
            )
        
        # TODO: Validate request

        gift_cards = await gift_card_service.get_gift_cards(request, db)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=BaseResponse(
                status=200,
                message="Gift cards retrieved successfully",
                data= gift_cards.model_dump()
            ).model_dump()
        )
    except IntegrityError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponse(
                status=400,
                message=f"Could not get gift cards - {e.orig}",
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
    
