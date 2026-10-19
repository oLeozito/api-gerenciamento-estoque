import logging
import sys
from pathlib import Path

# Garante que o Python encontre o módulo 'app' rodando como script
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def criar_admin_inicial(db: Session) -> None:
    repository = UsuarioRepository(db)
    admin_existente = repository.get_by_usuario(settings.admin_user)
    
    if admin_existente:
        logger.info("Usuario admin ja existe. Nenhuma acao necessaria.")
        return

    novo_admin = Usuario(
        nome=settings.admin_nome,
        usuario=settings.admin_user,
        senha_hash=get_password_hash(settings.admin_senha),
        cargo="admin"
    )
    
    repository.create(novo_admin)
    logger.info("Usuario admin criado com sucesso.")

def main() -> None:
    logger.info("Iniciando criacao do usuario administrador inicial...")
    db = SessionLocal()
    try:
        criar_admin_inicial(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()