from pathlib import Path
from utils import extrair_linhas_pdf

linhas = extrair_linhas_pdf(
    Path("data/entrada/nubank/Nubank_2026-01-04.pdf")
)

print(len(linhas))
print(linhas[:5])
