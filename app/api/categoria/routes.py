from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services.categoria_service import CategoriaService
from app.repositories.categoria_repository import CategoriaRepository
from app.api.deps import obter_usuario_logado, exigir_cargos # Importe o exigir_cargos
from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("", response_model=list[CategoriaResponse], status_code=status.HTTP_200_OK)
def listar_categorias(
    db: Session = Depends(get_db),
    # Qualquer logado pode listar
    usuario_atual: Usuario = Depends(obter_usuario_logado) 
):
    repository = CategoriaRepository(db)
    service = CategoriaService(repository)
    return service.listar_todas()

@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria_in: CategoriaCreate,
    db: Session = Depends(get_db),
    # Apenas admin e gerente passam daqui
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = CategoriaRepository(db)
    service = CategoriaService(repository)
    # Não precisamos mais passar autor_cargo
    return service.criar_categoria(categoria_in=categoria_in)

@router.put("/{id}", response_model=CategoriaResponse, status_code=status.HTTP_200_OK)
def atualizar_categoria(
    id: UUID,
    categoria_in: CategoriaUpdate,
    db: Session = Depends(get_db),
    # Apenas admin e gerente passam daqui
    usuario_atual: Usuario = Depends(exigir_cargos(["admin", "gerente"]))
):
    repository = CategoriaRepository(db)
    service = CategoriaService(repository)
    return service.atualizar_categoria(id=id, categoria_in=categoria_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(
    id: UUID,
    db: Session = Depends(get_db),
    # Apenas admin passa daqui
    usuario_atual: Usuario = Depends(exigir_cargos(["admin"]))
):
    repository = CategoriaRepository(db)
    service = CategoriaService(repository)
    service.deletar_categoria(id=id)