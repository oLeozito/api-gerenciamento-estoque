from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.token import TokenPayload
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
from app.core.database import get_db

# Diz ao FastAPI (e ao Swagger) onde fica a rota de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def obter_usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        token_data = TokenPayload(sub=user_id, role=payload.get("role"))
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    repository = UsuarioRepository(db)
    usuario = repository.get_by_id(token_data.sub)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
        
    return usuario