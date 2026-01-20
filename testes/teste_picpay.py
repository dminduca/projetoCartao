from pathlib import Path
from parsers.picpay_parser import PicPayParser

pdf = Path("input/faturas_pdf/PicPay_Fatura_122025.pdf")

parser = PicPayParser(pdf)
lancamentos = parser.parse()

for l in lancamentos:
    print(l)
