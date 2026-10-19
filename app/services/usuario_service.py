from fastapi import HTTPException, status
from app.schemas.usuario import UsuarioCreate
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import get_password_hash

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def criar_usuario(self, usuario_in: UsuarioCreate, autor_cargo: str) -> Usuario:
        # Regra de Negócio RBAC
        if autor_cargo == "estoquista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Estoquistas não têm permissão para cadastrar usuários."
            )
            
        if autor_cargo == "gerente" and usuario_in.cargo in ["admin", "gerente"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gerentes só podem cadastrar estoquistas."
            )

        # Regra de Negócio: Usuário já existe?
        if self.repository.get_by_usuario(usuario_in.usuario):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este nome de usuário já está em uso."
            )

        # Prepara o modelo para salvar
        novo_usuario = Usuario(
            nome=usuario_in.nome,
            usuario=usuario_in.usuario,
            senha_hash=get_password_hash(usuario_in.senha),
            cargo=usuario_in.cargo
        )
        
        return self.repository.create(novo_usuario)