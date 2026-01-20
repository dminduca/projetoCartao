import re
from typing import List

from modelos import LancamentoCartao
from parsers.parser_base import ParserBase
from utils import converter_data_nubank, converter_valor_para_float, converter_data_completa
from datetime import timedelta

# ----------------------------------
# Regex específica Nubank
# ----------------------------------
PADRAO_INICIO_TRANSACOES = re.compile(
    r"TRANSAÇÕES DE \d{2}\s+[A-Z]{3}\s+A\s+\d{2}\s+[A-Z]{3}",
    re.IGNORECASE
)

PADRAO_NUBANK = re.compile(
    r"(?P<data>\d{2}\s+[A-Z]{3})\s+"
    r"(?P<cartao>•{4}\s*\d{4})?\s*"
    r"(?P<descricao>.+?)\s+"
    r"R\$\s*(?P<valor>[\d\.,]+)",
    re.UNICODE,
)

PADRAO_VENCIMENTO = re.compile(
    r"Data de vencimento:\s*(?P<venc>\d{2}\s+[A-Z]{3}\s+\d{4})",
    re.IGNORECASE
)

class NubankParser(ParserBase):

    BANCO = "Nubank"
    
    def __init__(self, caminho_pdf, categorizador):
        super().__init__(caminho_pdf, categorizador)

    def parse(self) -> List[LancamentoCartao]:
        linhas = self._extrair_linhas_pdf()
        cartao_padrao = self._extrair_cartao_padrao(linhas)
        
        vencimento_str = self._extrair_data_vencimento(linhas)
        data_vencimento = (
            converter_data_completa(vencimento_str)
            if vencimento_str
            else None
        )

        registros: List[LancamentoCartao] = []
        dentro_transacoes = False

        for linha in linhas:
            
            # 🧠 Detecta início da seção correta
            if PADRAO_INICIO_TRANSACOES.search(linha):
                dentro_transacoes = True
                continue

            # ❌ Ignora tudo fora do bloco de transações
            if not dentro_transacoes:
                continue
            
            # 🔎 Aplica regex apenas no bloco correto
            match = PADRAO_NUBANK.search(linha)
            if not match:
                continue

            data = converter_data_nubank(
                match.group("data"),
                self.nome_arquivo
            )
            
            # Ajuste de ano para lançamentos Nubank
            if data_vencimento and data > data_vencimento:
                data = data.replace(year=data.year - 1)

            descricao = match.group("descricao").strip()
            valor = converter_valor_para_float(
                match.group("valor")
            )

            cartao = (
                match.group("cartao")
                or cartao_padrao
                or "•••• 0000"
            ).strip()

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
    # Métodos auxiliares Nubank
    # ----------------------------------
    def _extrair_cartao_padrao(self, linhas: List[str]) -> str | None:
        for linha in linhas:
            m = re.search(r"(•{4}\s*\d{4})", linha)
            if m:
                return m.group(1)
        return None
    
    def _extrair_data_vencimento(self, linhas: List[str]) -> str | None:
        for linha in linhas:
            m = PADRAO_VENCIMENTO.search(linha)
            if m:
                return m.group("venc")
        return None
