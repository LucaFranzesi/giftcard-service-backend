import uuid
from utils.converters import serialize_sqlalchemy_obj
from models.responses import TableResponse
from models.requests import GetListPaginatedRequest
from models.database import GiftCard

async def get_gift_cards_data(db):
    return db.query(GiftCard).filter(GiftCard.is_deleted == False)

async def create_gift_card(create_gift_card_request, db):
    
    create_gift_card_model = GiftCard(
        code = uuid.uuid4(),
        residual_amount = create_gift_card_request.amount,
        expiration = create_gift_card_request.expiration
    )

    db.add(create_gift_card_model)
    db.commit()

    return create_gift_card_model

async def get_gift_card(code: str, db):
    return db.query(GiftCard).filter(GiftCard.code == code).first()

async def get_gift_cards(request : GetListPaginatedRequest, db):
    items_to_take = request.items or 0
    items_to_skip = items_to_take * ((request.page or 1) - 1)
    
    gift_cards = await get_gift_cards_data(db)

    if request.filters and len(request.filters) > 0:
        for field, value in request.filters.items():
            if field:
                match field.lower():
                    # NOTE: Eventually add filters here
                    case _:
                        pass

    if request.search != None:
        gift_cards = gift_cards.filter(
            GiftCard.code.contains(request.search.lower())
            #TODO: Match with patient name
        )

    total = gift_cards.count()

    if items_to_skip > 0:
        gift_cards.skip(items_to_skip)

    if items_to_take > 0:
        gift_cards.take(items_to_take)

    items = [serialize_sqlalchemy_obj(gift_card) for gift_card in gift_cards.all() ]
    return TableResponse[dict](
        total = total,
        items = items
    )