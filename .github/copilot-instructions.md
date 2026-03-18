# Copilot Instructions - GiftCard Service Backend

## Architettura

Backend FastAPI per la gestione di Gift Cards con autenticazione JWT. Stack: FastAPI + SQLAlchemy + PostgreSQL.

### Struttura principale
```
app/
├── configurations/   # Config per ambiente (local/dev/prod) via APP_ENV
├── db/              # Engine SQLAlchemy e session factory
├── models/
│   ├── database/    # Modelli SQLAlchemy (Base da base.py)
│   ├── requests/    # Pydantic request DTOs
│   └── responses/   # Pydantic response DTOs
├── routers/         # Endpoint API (prefix + tags)
├── services/        # Business logic
└── utils/           # Helpers (encryption, converters)
```

## Pattern da seguire

### Configurazione ambiente
- La config è caricata in `configurations/__init__.py` via `APP_ENV` da `.env`
- Ogni ambiente (`local.py`, `development.py`, `production.py`) estende `BaseConfig`
- Accesso: `from configurations import config` → `config.DATABASE_URI`

### Modelli Database
- Tutti i modelli ereditano da `models.database.base.Base`
- Supporto soft-delete con campi `is_deleted`, `deleted_at` (vedi [database.dbml](../documents/database.dbml))
- I modelli vengono creati automaticamente: `Base.metadata.create_all(bind=engine)` in `main.py`

### API Response Pattern
Tutte le risposte usano `BaseResponse` con struttura consistente:
```python
return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content=BaseResponse(
        status=201,
        message="Success message",
        data=jsonable_encoder(serialize_sqlalchemy_obj(obj))
    ).model_dump()
)
```

### Dependency Injection
- `db_dependency`: sessione database (vedi [dependencies.py](../app/dependencies.py))
- `user_service.user_dependency`: utente autenticato da JWT
- `form_data_dependency`: per login OAuth2

### Autenticazione
- JWT con `python-jose`, bcrypt per password
- Token endpoint: `POST /auth/token` (OAuth2PasswordRequestForm)
- Ruoli: `admin`, `user` - controllo inline nei router
- Config secrets: `BCRYPT_SECRET_KEY`, `BCRYPT_ALGORITHM`

### Serializzazione SQLAlchemy → JSON
Usa sempre `serialize_sqlalchemy_obj()` da `utils/converters.py` per convertire oggetti SQLAlchemy in dict serializzabili.

## Comandi

```bash
# Avvio locale (dalla root)
cd app && uvicorn main:app --reload

# Database: PostgreSQL richiesto per local/dev/prod
# SQLite default solo in BaseConfig
```

## Convenzioni

- **Router**: prefix con nome risorsa (`/gift-cards`, `/auth`), tag per Swagger
- **Services**: funzioni async per business logic, query database dirette
- **Requests**: Pydantic `BaseModel` per validazione input
- **Liste paginate**: usa `GetListPaginatedRequest` e `TableResponse[T]`
- **Error handling**: catch `IntegrityError` per constraint violations
