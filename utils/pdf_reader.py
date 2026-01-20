from pathlib import Path
from typing import List

import pdfplumber


def extrair_linhas_pdf(caminho_pdf: Path) -> List[str]:
    """
    Extrai o texto de um PDF e retorna
    uma lista de linhas limpas (sem vazios).
    """
    linhas: List[str] = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text() or ""
            for linha in texto.splitlines():
                linha = linha.strip()
                if linha:
                    linhas.append(linha)

    return linhas
