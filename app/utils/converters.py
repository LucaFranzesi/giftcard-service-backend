from datetime import datetime

def serialize_sqlalchemy_obj(obj):
    """
    Converts SQLAlchemy object to a dictionary, handling special types like datetime.
    """
    if hasattr(obj, '__table__'):
        result = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            # Converte datetime in stringa ISO 8601
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    raise ValueError("Object is not an instance of a SQLAlchemy object.")