from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# O Pydantic já garantiu que a database_url existe e está correta
engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Injeta a sessão do banco nas rotas do FastAPI.
    O 'yield' entrega a sessão para a rota usar, e o 'finally' garante
    que a conexão com o PostgreSQL seja fechada quando a rota terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()