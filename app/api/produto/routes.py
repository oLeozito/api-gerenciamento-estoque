from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoListResponse, ProdutoDetailResponse
from app.services.produto_service import ProdutoService
from app.repositories.produto_repository import ProdutoRepository
from app.api.deps import obter_usuario_logado, exigir_cargos
from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("", response_model=list[ProdutoListResponse], status_code=status.HTTP_200_OK)
def listar_produtos(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = ProdutoRepository(db)
    service = ProdutoService(repository)
    return service.listar_todos()

@router.get("/{id}", response_model=ProdutoDetailResponse, status_code=status.HTTP_200_OK)
def buscar_produto(
    id: UUID,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = ProdutoRepository(db)
    service = ProdutoService(repository)
    return service.buscar_por_id(id)

@router.post("", response_model=ProdutoDetailResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto_in: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = ProdutoRepository(db)
    service = ProdutoService(repository)
    return service.criar_produto(produto_in=produto_in)

@router.patch("/{id}", response_model=ProdutoDetailResponse, status_code=status.HTTP_200_OK)
def atualizar_produto(
    id: UUID,
    produto_in: ProdutoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = ProdutoRepository(db)
    service = ProdutoService(repository)
    return service.atualizar_produto(id=id, produto_in=produto_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    id: UUID,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["admin"]))
):
    repository = ProdutoRepository(db)
    service = ProdutoService(repository)
    service.deletar_produto(id=id)