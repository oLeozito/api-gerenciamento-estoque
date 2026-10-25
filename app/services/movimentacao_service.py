from uuid import UUID
from fastapi import HTTPException, status

from datetime import datetime
from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate, TipoMovimentacao
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.repositories.produto_repository import ProdutoRepository

class MovimentacaoService:
    def __init__(self, repository: MovimentacaoRepository, produto_repo: ProdutoRepository):
        self.repository = repository
        self.produto_repo = produto_repo

    def listar_todas(
        self, 
        data_inicio: datetime | None = None, 
        data_fim: datetime | None = None, 
        tipo: str | None = None, 
        fornecedor_id: UUID | None = None
    ) -> list[Movimentacao]:
        return self.repository.pesquisar_avancado(data_inicio, data_fim, tipo, fornecedor_id)

    def buscar_por_produto(self, produto_id: UUID) -> list[Movimentacao]:
        return self.repository.get_by_produto_id(produto_id)

    def criar_movimentacao(self, mov_in: MovimentacaoCreate, usuario_id: UUID) -> Movimentacao:
        produto = self.produto_repo.get_by_id(mov_in.produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")

        if mov_in.tipo == TipoMovimentacao.SAIDA:
            if produto.qtd_estoque < mov_in.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente. O produto possui apenas {produto.qtd_estoque} unidades."
                )
            produto.qtd_estoque -= mov_in.quantidade
            mov_in.valor_unitario = produto.preco_venda
        
        elif mov_in.tipo == TipoMovimentacao.ENTRADA:
            produto.qtd_estoque += mov_in.quantidade

            if mov_in.valor_unitario is not None:
                produto.preco_custo = mov_in.valor_unitario

        nova_movimentacao = Movimentacao(
            tipo=mov_in.tipo.value,
            quantidade=mov_in.quantidade,
            valor_unitario=mov_in.valor_unitario,
            produto_id=mov_in.produto_id
            usuario_id=usuario_id
        )
        
        self.repository.session.add(nova_movimentacao)
        self.repository.session.commit()
        self.repository.session.refresh(nova_movimentacao)

        return nova_movimentacao