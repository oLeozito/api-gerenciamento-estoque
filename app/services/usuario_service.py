from uuid import UUID
from fastapi import HTTPException, status
from app.schemas.usuario import UsuarioCreate
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import get_password_hash

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def criar_usuario(self, usuario_in: UsuarioCreate, autor_cargo: str) -> Usuario:
        if autor_cargo == "gerente" and usuario_in.cargo in ["admin", "gerente"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gerentes só podem cadastrar estoquistas."
            )

        if self.repository.get_by_usuario(usuario_in.usuario):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este nome de usuário já está em uso."
            )

        novo_usuario = Usuario(
            nome=usuario_in.nome,
            usuario=usuario_in.usuario,
            senha_hash=get_password_hash(usuario_in.senha),
            cargo=usuario_in.cargo
        )
        
        return self.repository.create(novo_usuario)

    def listar_usuarios(self):
        return self.repository.listar_todos()

    def atualizar_usuario(self, usuario_id: UUID, dados: dict, autor_cargo: str) -> Usuario:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        if autor_cargo == "gerente" and (usuario.cargo == "admin" or dados["cargo"] == "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Sem permissão para alterar este cargo."
            )

        usuario.nome = dados["nome"]
        usuario.cargo = dados["cargo"]
        
        return self.repository.update(usuario)