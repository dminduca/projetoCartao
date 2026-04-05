import pandas as pd
from config import (
    BASE_HISTORICA_2025,
    PENDENCIAS_PATH
)
from utils import normalizar_texto

def normalizar_categoria(valor):
    if pd.isna(valor):
        return ""

    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    texto = str(valor).strip()

    if not texto or texto.lower() == "nan":
        return ""

    if texto.endswith(".0") and texto[:-2].isdigit():
        return texto[:-2]

    return texto

if not PENDENCIAS_PATH.exists():
    raise FileNotFoundError("Arquivo de pendências não encontrado.")

if not BASE_HISTORICA_2025.exists():
    raise FileNotFoundError("Base histórica não encontrada.")


df_pend = pd.read_excel(PENDENCIAS_PATH)
df_base = pd.read_excel(BASE_HISTORICA_2025, sheet_name="historico")

df_base["DescNormalizada"] = df_base["DescNormalizada"].astype(str)
df_base["IndCategoria"] = df_base["IndCategoria"].apply(normalizar_categoria)

categorias_validas = set(df_base["IndCategoria"].unique())
descricoes_existentes = set(df_base["DescNormalizada"].unique())

novos_registros = []
ignorados = 0


for _, row in df_pend.iterrows():
    ind_categoria = normalizar_categoria(row.get("IndCategoria", ""))

    if not ind_categoria:
        ignorados += 1
        continue

    if ind_categoria not in categorias_validas:
        print(f"⚠️ Categoria inválida ignorada: {ind_categoria}")
        ignorados += 1
        continue

    descricao_norm = normalizar_texto(row["DescNormalizada"])

    if descricao_norm in descricoes_existentes:
        ignorados += 1
        continue

    novos_registros.append({
        "DescNormalizada": descricao_norm,
        "IndCategoria": ind_categoria,
    })

    descricoes_existentes.add(descricao_norm)


if novos_registros:
    df_novos = pd.DataFrame(novos_registros)
    df_final = pd.concat([df_base, df_novos], ignore_index=True)
    df_final.to_excel(BASE_HISTORICA_2025, index=False, sheet_name="historico")

    print("✅ Importação concluída com sucesso!")
    print(f"➕ Novos registros inseridos: {len(novos_registros)}")
else:
    print("ℹ️ Nenhum novo registro para importar.")

print(f"⛔ Registros ignorados: {ignorados}")

# ==========================
# LIMPEZA DAS PENDÊNCIAS
# ==========================
PENDENCIAS_PATH.unlink()
print("🧹 Arquivo de pendências removido com sucesso.")