import re
from typing import List

from modelos import LancamentoCartao
from parsers.parser_base import ParserBase
from utils import (
    converter_data_picpay,
    converter_valor_para_float,
    converter_datav_picpay
)


REGEX_CARTAO_PICPAY = re.compile(
    r"Picpay\s+Card\s+final\s+(\d+)",
    re.IGNORECASE
)

REGEX_LANCAMENTO_PICPAY = re.compile(
    r"(?P<data>\d{2}/\d{2})\s+"
    r"(?P<descricao>.+?)\s+"
    r"(?P<valor>\d{1,3}(?:[.\d]*)?,\d{2})$"
)

PADRAO_VENCIMENTO_PICPAY = re.compile(
    r"Vencimento:\s*(\d{2}-\d{2}-\d{4})",
    re.IGNORECASE
)


class PicPayParser(ParserBase):

    BANCO = "PicPay"
    
    def __init__(self, caminho_pdf, categorizador):
        super().__init__(caminho_pdf, categorizador)

    def parse(self) -> List[LancamentoCartao]:
        linhas = self._extrair_linhas_pdf()
        numero_cartao = self._extrair_numero_cartao(linhas)
        
        data_venc_str = self._extrair_data_vencimento(linhas)
        data_vencimento = (
            converter_datav_picpay(data_venc_str)
            if data_venc_str
            else None
        )

        registros: List[LancamentoCartao] = []

        for linha in linhas:
            if self._linha_ignorada(linha):
                continue

            match = REGEX_LANCAMENTO_PICPAY.search(linha)
            if not match:
                continue

            data = converter_data_picpay(
                match.group("data"),
                self.nome_arquivo
            )

            descricao = self._tratar_descricao(
                match.group("descricao")
            )
            
            cartao = numero_cartao

            valor = converter_valor_para_float(
                match.group("valor")
            )

            resultado = self.categorizador.categorizar(descricao)

            lanc = LancamentoCartao(
                banco=self.BANCO,
                arquivo=self.nome_arquivo,
                data=data,
                cartao=cartao,
                descricao=descricao,
                valor=valor,
                data_vencimento=data_vencimento,
                desc_normalizada=resultado["DescBase"],
                categoria=resultado["Categoria"],
                ind_categoria=resultado["IndCategoria"],
                tipo_match=resultado["TipoMatch"],
                score_match=resultado["ScoreMatch"],
            )
            
            registros.append(lanc)

        return registros

    # ----------------------------------
    # Métodos auxiliares PicPay
    # ----------------------------------
    def _extrair_numero_cartao(self, linhas: List[str]) -> str:
        for linha in linhas:
            m = REGEX_CARTAO_PICPAY.search(linha)
            if m:
                return m.group(1)
        return ""

    def _linha_ignorada(self, linha: str) -> bool:
        return any(
            x in linha
            for x in (
                "Transações Nacionais",
                "Data Estabelecimento",
                "Subtotal",
            )
        )

    def _tratar_descricao(self, descricao: str) -> str:
        """
        Substitui PARC09/10 por ' - Parcela 09/10'
        """
        return re.sub(
            r"PARC\s*(\d{2}/\d{2})",
            r" - Parcela \1",
            descricao,
            flags=re.IGNORECASE
        ).strip()
    
    def _extrair_data_vencimento(self, linhas: list[str]) -> str | None:
        for linha in linhas:
            m = PADRAO_VENCIMENTO_PICPAY.search(linha)
            if m:
                return m.group(1)  # 05-01-2026
        return None
