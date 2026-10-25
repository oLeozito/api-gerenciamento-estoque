from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.repositories.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def listar_todos(self) -> list[Produto]:
        return self.repository.get_all()

    def listar_estoque_baixo(self, limite: int) -> list[Produto]:
        return self.repository.get_estoque_baixo(limite)

    def buscar_por_id(self, id: UUID) -> Produto:
        produto = self.repository.get_by_id(id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")
        return produto

    def criar_produto(self, produto_in: ProdutoCreate) -> Produto:
        if self.repository.get_by_codigo(produto_in.codigo):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um produto com este código.")

        # O modelo assumirá qtd_estoque = 0 automaticamente
        novo_produto = Produto(**produto_in.model_dump())
        
        try:
            return self.repository.create(novo_produto)
        except IntegrityError:
            # Captura erro caso a categoria_id ou fornecedor_id enviada não exista no banco
            self.repository.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Categoria ou Fornecedor inválidos."
            )

    def atualizar_produto(self, id: UUID, produto_in: ProdutoUpdate) -> Produto:
        produto_db = self.buscar_por_id(id)

        if produto_in.codigo and produto_in.codigo != produto_db.codigo:
            if self.repository.get_by_codigo(produto_in.codigo):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O código informado já pertence a outro produto.")

        update_data = produto_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(produto_db, field, value)

        try:
            return self.repository.update(produto_db)
        except IntegrityError:
            self.repository.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Categoria ou Fornecedor inválidos."
            )

    def deletar_produto(self, id: UUID) -> None:
        produto_db = self.buscar_por_id(id)
        try:
            self.repository.delete(produto_db)
        except IntegrityError:
            self.repository.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não é possível excluir este produto pois existem movimentações vinculadas a ele."
            )