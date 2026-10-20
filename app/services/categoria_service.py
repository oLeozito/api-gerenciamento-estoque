from uuid import UUID
from fastapi import HTTPException, status

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.repositories.categoria_repository import CategoriaRepository

class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def listar_todas(self) -> list[Categoria]:
        return self.repository.get_all()

    def criar_categoria(self, categoria_in: CategoriaCreate) -> Categoria:
        if self.repository.get_by_nome(categoria_in.nome):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma categoria com este nome."
            )

        nova_categoria = Categoria(nome=categoria_in.nome)
        return self.repository.create(nova_categoria)

    def atualizar_categoria(self, id: UUID, categoria_in: CategoriaUpdate) -> Categoria:
        categoria_db = self.repository.get_by_id(id)
        if not categoria_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")

        if categoria_in.nome != categoria_db.nome and self.repository.get_by_nome(categoria_in.nome):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outra categoria com este nome."
            )

        categoria_db.nome = categoria_in.nome
        return self.repository.update(categoria_db)

    def deletar_categoria(self, id: UUID) -> None:
        categoria_db = self.repository.get_by_id(id)
        if not categoria_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")

        self.repository.delete(categoria_db)