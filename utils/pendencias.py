import pandas as pd
from utils import normalizar_texto
from config import PENDENCIAS_PATH


def registrar_pendencias(lancamentos):
    pendencias = []

    for l in lancamentos:
        if l.categoria != "NÃO CLASSIFICADO":
            continue

        pendencias.append({
            "banco": l.banco,
            "arquivo": l.arquivo,
            "data": l.data,
            "descricao_original": l.descricao,
            "descricao_normalizada": normalizar_texto(l.descricao),
        })

    if not pendencias:
        return

    df_novo = pd.DataFrame(pendencias)

    if PENDENCIAS_PATH.exists():
        df_existente = pd.read_excel(PENDENCIAS_PATH)
        df_final = pd.concat([df_existente, df_novo]).drop_duplicates(
            subset=["descricao_normalizada"]
        )
    else:
        df_final = df_novo

    df_final.to_excel(PENDENCIAS_PATH, index=False)
