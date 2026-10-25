from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate, FornecedorListResponse, FornecedorDetailResponse
from app.services.fornecedor_service import FornecedorService
from app.repositories.fornecedor_repository import FornecedorRepository
from app.api.deps import obter_usuario_logado, exigir_cargos
from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

@router.get("", response_model=list[FornecedorListResponse], status_code=status.HTTP_200_OK)
def listar_fornecedores(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = FornecedorRepository(db)
    service = FornecedorService(repository)
    return service.listar_todos()

@router.get("/{id}", response_model=FornecedorDetailResponse, status_code=status.HTTP_200_OK)
def buscar_fornecedor(
    id: UUID,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = FornecedorRepository(db)
    service = FornecedorService(repository)
    return service.buscar_por_id(id)

@router.post("", response_model=FornecedorDetailResponse, status_code=status.HTTP_201_CREATED)
def criar_fornecedor(
    fornecedor_in: FornecedorCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = FornecedorRepository(db)
    service = FornecedorService(repository)
    return service.criar_fornecedor(fornecedor_in=fornecedor_in)

@router.patch("/{id}", response_model=FornecedorDetailResponse, status_code=status.HTTP_200_OK)
def atualizar_fornecedor(
    id: UUID,
    fornecedor_in: FornecedorUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = FornecedorRepository(db)
    service = FornecedorService(repository)
    return service.atualizar_fornecedor(id=id, fornecedor_in=fornecedor_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_fornecedor(
    id: UUID,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin"]))
):
    repository = FornecedorRepository(db)
    service = FornecedorService(repository)
    service.deletar_fornecedor(id=id)