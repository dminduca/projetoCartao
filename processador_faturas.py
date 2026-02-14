from pathlib import Path

from parsers.nubank_parser import NubankParser
from parsers.picpay_parser import PicPayParser
from modelos import LancamentoCartao
from categorizador import Categorizador
from config import PROCESSADOS_DIR


class ProcessadorFaturas:
    
    def __init__(self, categorizador: Categorizador):
        self.categorizador = categorizador

    # ---------------------------------
    # 🔹 Identificação do parser
    # ---------------------------------
    def identificar_parser(self, pdf_path: Path):
        nome = pdf_path.name.lower()

        if "nubank" in nome:
            return NubankParser(pdf_path, self.categorizador)

        if "picpay" in nome:
            return PicPayParser(pdf_path, self.categorizador)

        raise ValueError(f"Banco não identificado: {pdf_path.name}")


    # ---------------------------------
    # 🔹 Execução principal
    # ---------------------------------
    def processar_pasta(self, pasta_pdf: Path) -> list[LancamentoCartao]:
        lancamentos = []
        pendencias = []


        if not pasta_pdf.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {pasta_pdf}")

        for pdf_path in sorted(pasta_pdf.glob("*.pdf")):
            print(f"📄 Processando: {pdf_path.name}")

            parser = self.identificar_parser(pdf_path)
            registros = parser.parse()

            self._mover_para_processados(pdf_path, parser.BANCO)

            lancamentos.extend(registros)
            
            for l in registros:
                if l.ind_categoria is None:
                    pendencias.append({
                        "Banco": l.banco,
                        "DescricaoOriginal": l.descricao,
                        "DescNormalizada": l.desc_normalizada,
                        "Arquivo": l.arquivo,
                        "IndCategoria": "",  # para preenchimento manual
                    })

        return lancamentos, pendencias

    # ---------------------------------
    # 🔹 Pós-processamento
    # ---------------------------------
    def _mover_para_processados(self, pdf_path: Path, banco: str):
        destino_dir = PROCESSADOS_DIR / banco.lower()
        destino_dir.mkdir(parents=True, exist_ok=True)

        destino = destino_dir / pdf_path.name
        pdf_path.rename(destino)
