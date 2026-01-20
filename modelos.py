from dataclasses import dataclass
from datetime import date


@dataclass
class LancamentoCartao:
    def __init__(
        self,
        banco: str,
        arquivo: str,
        data,
        cartao: str,
        descricao: str,
        valor: float,
        data_vencimento=None,
        categoria: str = "Não classificado",
        formPagto: str = "3 - Crédito",
        operacao: str = "Despesa",
        status: str = "1 - Pendente",
        desc_normalizada: str | None = None,
        ind_categoria: int | None = None,
        tipo_match: str | None = None,
        score_match: int | None = None,
    ):
        self.banco = banco
        self.arquivo = arquivo
        self.data = data
        self.cartao = cartao
        self.descricao = descricao
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.categoria = categoria
        self.formPagto = formPagto
        self.operacao = operacao
        self.status = status
        self.desc_normalizada = desc_normalizada
        self.ind_categoria = ind_categoria
        self.tipo_match = tipo_match
        self.score_match = score_match

    def to_dict(self):
        return {
            "banco": self.banco,
            "arquivo": self.arquivo,
            "data": self.data,
            "cartao": self.cartao,
            "descricao": self.descricao,
            "valor": self.valor,
            "data_vencimento": self.data_vencimento,
            "categoria": self.categoria,
            "formPagto": self.formPagto,
            "operacao": self.operacao,
            "status": self.status,
            "desc_normalizada": self.desc_normalizada,
            "ind_categoria": self.ind_categoria,
            "tipo_match": self.tipo_match,
            "score_match": self.score_match,
        }

