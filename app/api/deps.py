from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.token import TokenPayload
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
from app.core.database import get_db

# Removemos o OAuth2PasswordBearer e ativamos o esquema Bearer genérico
security_scheme = HTTPBearer()

def obter_usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    # O token é agora extraído diretamente das credenciais
    token = credenciais.credentials
    
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
            detail="Utilizador não encontrado",
        )
        
    return usuario

def exigir_cargos(cargos_permitidos: list[str]):
    def validador(usuario: Usuario = Depends(obter_usuario_logado)) -> Usuario:
        if usuario.cargo not in cargos_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado. Você não tem permissão para realizar esta ação."
            )
        return usuario
    return validador