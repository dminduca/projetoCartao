import pandas as pd

from config import (
    FATURAS_PDF_DIR,
    OUTPUT_DIR,
    BASE_HISTORICA_2025,
    CATEGORIAS_2026,
)

from categorizador import Categorizador
from processador_faturas import ProcessadorFaturas


def main():
    print("🚀 Iniciando pipeline de processamento de faturas...\n")

    # -------------------------------------------------
    # 1️⃣ Inicializa serviços
    # -------------------------------------------------
    categorizador = Categorizador(
        BASE_HISTORICA_2025,
        CATEGORIAS_2026,
    )

    processador = ProcessadorFaturas(
        categorizador=categorizador
    )

    # -------------------------------------------------
    # 2️⃣ Processa PDFs
    # -------------------------------------------------
    lancamentos, pendencias = processador.processar_pasta(FATURAS_PDF_DIR)

    print(f"\n📊 Total de lançamentos processados: {len(lancamentos)}")

    if not lancamentos:
        print("⚠️ Nenhum lançamento encontrado. Encerrando.")
        return

    # -------------------------------------------------
    # 3️⃣ Exporta resultado
    # -------------------------------------------------
    df = pd.DataFrame([l.to_dict() for l in lancamentos])
    
    df["data"] = pd.to_datetime(df["data"])
    df["data_vencimento"] = pd.to_datetime(df["data_vencimento"])

    arquivo_saida = OUTPUT_DIR / "lancamentos.xlsx"
    df.to_excel(arquivo_saida, index=False)

    print(f"\n📁 Arquivo gerado com sucesso:")
    print(f"➡️ {arquivo_saida.resolve()}")
    
    if pendencias:
        df_pend = pd.DataFrame(pendencias)
        caminho_pend = OUTPUT_DIR / "pendencias_categorizacao.xlsx"
        df_pend.to_excel(caminho_pend, index=False)

        print(f"⚠️ Pendências de categorização geradas:")
        print(f"➡️ {caminho_pend.resolve()}")

if __name__ == "__main__":
    main()
