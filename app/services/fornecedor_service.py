from uuid import UUID
from fastapi import HTTPException, status

from app.models.fornecedor import Fornecedor
from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate
from app.repositories.fornecedor_repository import FornecedorRepository

class FornecedorService:
    def __init__(self, repository: FornecedorRepository):
        self.repository = repository

    def listar_todos(self) -> list[Fornecedor]:
        return self.repository.get_all()

    def buscar_por_id(self, id: UUID) -> Fornecedor:
        fornecedor = self.repository.get_by_id(id)
        if not fornecedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado.")
        return fornecedor

    def criar_fornecedor(self, fornecedor_in: FornecedorCreate) -> Fornecedor:
        if self.repository.get_by_cnpj(fornecedor_in.cnpj):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um fornecedor com este CNPJ.")
        
        if self.repository.get_by_email(fornecedor_in.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um fornecedor com este e-mail.")

        novo_fornecedor = Fornecedor(
            nome=fornecedor_in.nome,
            cnpj=fornecedor_in.cnpj,
            telefone=fornecedor_in.telefone,
            email=fornecedor_in.email
        )
        return self.repository.create(novo_fornecedor)

    def atualizar_fornecedor(self, id: UUID, fornecedor_in: FornecedorUpdate) -> Fornecedor:
        fornecedor_db = self.buscar_por_id(id)

        if fornecedor_in.cnpj and fornecedor_in.cnpj != fornecedor_db.cnpj:
            if self.repository.get_by_cnpj(fornecedor_in.cnpj):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O CNPJ informado já pertence a outro fornecedor.")
        
        if fornecedor_in.email and fornecedor_in.email != fornecedor_db.email:
            if self.repository.get_by_email(fornecedor_in.email):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O e-mail informado já pertence a outro fornecedor.")

        update_data = fornecedor_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(fornecedor_db, field, value)

        return self.repository.update(fornecedor_db)

    def deletar_fornecedor(self, id: UUID) -> None:
        fornecedor_db = self.buscar_por_id(id)
        self.repository.delete(fornecedor_db)