from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioLogin, UsuarioCreate, UsuarioResponse
from app.schemas.token import Token
from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository
from app.api.deps import obter_usuario_logado
from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token)
def login(
    credenciais: UsuarioLogin,
    db: Session = Depends(get_db)
):
    repository = UsuarioRepository(db)
    service = AuthService(repository)
    
    token = service.autenticar_usuario(
        usuario=credenciais.usuario,
        senha_plana=credenciais.senha
    )
    return {"access_token": token, "token_type": "bearer"}
    
@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    usuario_in: UsuarioCreate,
    usuario_atual: Usuario = Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    
    novo_usuario = service.criar_usuario(
        usuario_in=usuario_in,
        autor_cargo=usuario_atual.cargo
    )
    return novo_usuario