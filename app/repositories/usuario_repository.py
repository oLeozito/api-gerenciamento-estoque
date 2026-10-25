from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_usuario(self, usuario: str) -> Usuario | None:
        query = select(Usuario).where(Usuario.usuario == usuario)
        result = self.session.execute(query).scalar_one_or_none()
        return result

    def get_by_id(self, id: str) -> Usuario | None:
        query = select(Usuario).where(Usuario.id == id)
        result = self.session.execute(query).scalar_one_or_none()
        return result

    def create(self, usuario_model: Usuario) -> Usuario:
        self.session.add(usuario_model)
        self.session.commit()
        self.session.refresh(usuario_model)
        return usuario_model

    def listar_todos(self) -> list[Usuario]:
        query = select(Usuario)
        return list(self.session.execute(query).scalars().all())