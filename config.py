from pathlib import Path

BASE_DIR = Path(__file__).parent

# Entrada
INPUT_DIR = BASE_DIR / "input"
FATURAS_PDF_DIR = INPUT_DIR / "faturas_pdf"

# Processados
PROCESSADOS_DIR = INPUT_DIR / "faturas_processadas"

# Saída
OUTPUT_DIR = BASE_DIR / "output"

# -------------------------
# Bases de categorização
# -------------------------
CATEGORIAS_DIR = BASE_DIR / "data" / "categorias"


BASE_HISTORICA_2025 = CATEGORIAS_DIR / "base_2025_normalizada.xlsx"
CATEGORIAS_2026 = CATEGORIAS_DIR / "categorias_2026.xlsx"
PENDENCIAS_PATH = OUTPUT_DIR / "pendencias_categorizacao.xlsx"

# Criação automática das pastas
for pasta in [
    FATURAS_PDF_DIR,
    PROCESSADOS_DIR,
    OUTPUT_DIR,
]:
    pasta.mkdir(parents=True, exist_ok=True)
