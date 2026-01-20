import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from categorizador import Categorizador



# 📌 Fixture: cria uma instância reutilizável do categorizador
@pytest.fixture(scope="session")
def categorizador():
    return Categorizador(
        Path("data/categorias/base_2025_normalizada.xlsx"),
        Path("data/categorias/categorias_2026.xlsx"),
    )


# -------------------------------------------------
# 🔹 Teste: match exato
# -------------------------------------------------
def test_categorizacao_exata(categorizador):
    resultado = categorizador.categorizar("Mercadoe")

    assert resultado["Categoria"] == "Alimentação"
    assert resultado["TipoMatch"] == "EXATO"
    assert resultado["ScoreMatch"] == 100


# -------------------------------------------------
# 🔹 Teste: fuzzy matching
# -------------------------------------------------
def test_categorizacao_fuzzy(categorizador):
    resultado = categorizador.categorizar("Shibata Comercio")

    assert resultado["Categoria"] == "Alimentação"
    assert resultado["TipoMatch"] in ("FUZZY", "EXATO")
    assert resultado["ScoreMatch"] >= categorizador.SCORE_MINIMO


# -------------------------------------------------
# 🔹 Teste: não classificado
# -------------------------------------------------
def test_nao_classificado(categorizador):
    resultado = categorizador.categorizar("Descricao Totalmente Inexistente")

    assert resultado["Categoria"] == "Não classificado"
    assert resultado["TipoMatch"] == "NÃO CLASSIFICADO"
    assert resultado["IndCategoria"] is None
