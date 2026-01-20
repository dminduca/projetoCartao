from pathlib import Path
from typing import List
import pdfplumber


class ParserBase:
    BANCO = "BASE"

    def __init__(self, caminho_pdf: Path, categorizador):
        self.caminho_pdf = caminho_pdf
        self.nome_arquivo = caminho_pdf.name
        self.categorizador = categorizador  # 🧠 serviço de categorização

    def parse(self):
        """
        Deve ser implementado pelos parsers específicos (Nubank, PicPay, etc)
        """
        raise NotImplementedError

    # 🔑 MÉTODO COMUM A TODOS OS PARSERS
    def _extrair_linhas_pdf(self) -> List[str]:
        linhas = []

        with pdfplumber.open(self.caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text() or ""
                for linha in texto.splitlines():
                    linha = linha.strip()
                    if linha:
                        linhas.append(linha)

        return linhas
