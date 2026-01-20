from pathlib import Path
from parsers.nubank_parser import NubankParser

pdf = Path("input/faturas_pdf/Nubank_2026-01-04.pdf")

parser = NubankParser(pdf)
lancamentos = parser.parse()

for l in lancamentos:
    print(l)
