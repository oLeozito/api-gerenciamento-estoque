from uuid import UUID
from fastapi import HTTPException, status

from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate, TipoMovimentacao
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.repositories.produto_repository import ProdutoRepository

class MovimentacaoService:
    def __init__(self, repository: MovimentacaoRepository, produto_repo: ProdutoRepository):
        self.repository = repository
        self.produto_repo = produto_repo

    def listar_todas(self) -> list[Movimentacao]:
        return self.repository.get_all()

    def buscar_por_produto(self, produto_id: UUID) -> list[Movimentacao]:
        return self.repository.get_by_produto_id(produto_id)

    def criar_movimentacao(self, mov_in: MovimentacaoCreate) -> Movimentacao:
        # 1. Busca o produto
        produto = self.produto_repo.get_by_id(mov_in.produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")

        # 2. Valida regras matemáticas de estoque
        if mov_in.tipo == TipoMovimentacao.SAIDA:
            if produto.qtd_estoque < mov_in.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente. O produto possui apenas {produto.qtd_estoque} unidades."
                )
            # Deduz do estoque
            produto.qtd_estoque -= mov_in.quantidade
        
        elif mov_in.tipo == TipoMovimentacao.ENTRADA:
            # Adiciona ao estoque
            produto.qtd_estoque += mov_in.quantidade

            if mov_in.valor_unitario is not None:
                produto.preco_custo = mov_in.valor_unitario

        # 3. Cria a entidade de movimentação
        nova_movimentacao = Movimentacao(
            tipo=mov_in.tipo.value,
            quantidade=mov_in.quantidade,
            valor_unitario=mov_in.valor_unitario,
            produto_id=mov_in.produto_id
        )
        
        # 4. Salva a movimentação E a alteração do produto na MESMA transação
        self.repository.session.add(nova_movimentacao)
        self.repository.session.commit()
        self.repository.session.refresh(nova_movimentacao)

        return nova_movimentacao