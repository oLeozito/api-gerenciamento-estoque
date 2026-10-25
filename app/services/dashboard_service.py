from collections import defaultdict
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.movimentacao_repository import MovimentacaoRepository

class DashboardService:
    def __init__(self, prod_repo: ProdutoRepository, mov_repo: MovimentacaoRepository):
        self.prod_repo = prod_repo
        self.mov_repo = mov_repo

    def gerar_dashboard(self) -> dict:
        top_vendas = self.mov_repo.get_produto_mais_vendido_30_dias()
        dados_diarios = self.mov_repo.get_agrupamento_diario_30_dias()
        estoque_critico = self.prod_repo.get_estoque_critico_count()
        estoque_atual = self.prod_repo.get_all_simplificado()

        diario_dict = defaultdict(lambda: {"entradas_qtd": 0, "entradas_rs": 0.0, "saidas_qtd": 0, "saidas_rs": 0.0})
        
        totais = {
            "entradas": {"quantidade": 0, "valor_reais": 0.0},
            "saidas": {"quantidade": 0, "valor_reais": 0.0}
        }

        for dia, tipo, sum_qtd, sum_valor in dados_diarios:
            qtd = int(sum_qtd or 0)
            valor = float(sum_valor or 0.0)
            
            if tipo == "ENTRADA":
                diario_dict[dia]["entradas_qtd"] += qtd
                diario_dict[dia]["entradas_rs"] += valor
                totais["entradas"]["quantidade"] += qtd
                totais["entradas"]["valor_reais"] += valor
            else:
                diario_dict[dia]["saidas_qtd"] += qtd
                diario_dict[dia]["saidas_rs"] += valor
                totais["saidas"]["quantidade"] += qtd
                totais["saidas"]["valor_reais"] += valor

        grafico = [{"data": data, **valores} for data, valores in sorted(diario_dict.items())]

        produto_top = None
        if top_vendas:
            produto_top = {
                "id": top_vendas.id,
                "nome": top_vendas.nome,
                "quantidade_vendida": int(top_vendas.total_vendido)
            }

        estoque_formatado = [
            {"id": p.id, "nome": p.nome, "qtd_estoque": p.qtd_estoque} 
            for p in estoque_atual
        ]

        return {
            "produto_mais_vendido": produto_top,
            "totais_30_dias": totais,
            "grafico_diario": grafico,
            "estoque_atual": estoque_formatado,
            "produtos_estoque_critico": estoque_critico
        }