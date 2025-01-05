def serialize_sqlalchemy_obj(obj):
    """
    Converts SQLAlchemy object to a dictionary
    """
    if hasattr(obj, '__table__'):
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
    raise ValueError("Obj non è un'istanza di un modello SQLAlchemy.")