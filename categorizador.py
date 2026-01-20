from pathlib import Path
import re
import pandas as pd
from rapidfuzz import process, fuzz


class Categorizador:
    """
    Serviço responsável por categorizar despesas a partir da descrição,
    usando base histórica (match exato + fuzzy matching).
    """

    SCORE_MINIMO = 85  # ajuste fino aqui (80–90)

    def __init__(
        self,
        caminho_base_2025: Path,
        caminho_categorias: Path,
    ):
        self.mapa_descricao_categoria = {}
        self.categorias = {}
        self.descricoes_base = []

        self._carregar_base_2025(caminho_base_2025)
        self._carregar_categorias(caminho_categorias)
    
    # -------------------------------------------------
    # 🔹 Limpeza Descrição
    # -------------------------------------------------
    def remover_parcela(self, texto: str) -> str:
        """
        Remove sufixos como:
        - ' - Parcela 6/10'
        - 'PARC 2/3'
        - 'Parcela 01/12'
        """
        return re.sub(
            r"\s*[-–]?\s*parc(el(a)?)?\s*\d{1,2}\s*/\s*\d{1,2}",
            "",
            texto,
            flags=re.IGNORECASE,
        ).strip()


    # -------------------------------------------------
    # 🔹 Normalização
    # -------------------------------------------------
    def normalizar(self, texto: str) -> str:
        texto = str(texto).lower()
        texto = re.sub(r"[^a-z0-9\s*]", "", texto)
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    # -------------------------------------------------
    # 🔹 Carga da base histórica 2025
    # -------------------------------------------------
    def _carregar_base_2025(self, caminho: Path):
        if not caminho.exists():
            raise FileNotFoundError(f"Base 2025 não encontrada: {caminho}")

        df = pd.read_excel(caminho, sheet_name="historico")
        
        ignorados = 0

        for _, row in df.iterrows():
            try:
                desc_norm = self.normalizar(row["DescNormalizada"])
                ind_categoria = int(row["IndCategoria"])
            except (ValueError, TypeError):
                ignorados += 1
                continue
            
            self.mapa_descricao_categoria[desc_norm] = ind_categoria

        self.descricoes_base = list(self.mapa_descricao_categoria.keys())

        print(f"📘 Base 2025 carregada: {len(self.mapa_descricao_categoria)} descrições ({ignorados} ignoradas)")

    # -------------------------------------------------
    # 🔹 Carga da tabela de categorias
    # -------------------------------------------------
    def _carregar_categorias(self, caminho: Path):
        if not caminho.exists():
            raise FileNotFoundError(f"Tabela de categorias não encontrada: {caminho}")

        df = pd.read_excel(caminho)

        for _, row in df.iterrows():
            self.categorias[int(row["IndCategoria"])] = {
                "Categoria": row["Categoria"],
                "Lista": row["Lista"],
            }

        print(f"📗 Categorias carregadas: {len(self.categorias)}")

    # -------------------------------------------------
    # 🔹 Categorização principal
    # -------------------------------------------------
    def categorizar(self, descricao: str) -> dict:
        descricao_limpa = self.remover_parcela(descricao)
        desc_norm = self.normalizar(descricao_limpa)

        # 1️⃣ Match exato
        if desc_norm in self.mapa_descricao_categoria:
            ind = self.mapa_descricao_categoria[desc_norm]
            cat = self.categorias.get(ind, {})

            return {
                "IndCategoria": ind,
                "Categoria": cat.get("Lista"),
                "Lista": cat.get("Categoria"),
                "TipoMatch": "EXATO",
                "ScoreMatch": 100,
                "DescBase": desc_norm,
            }

        # 2️⃣ Match fuzzy
        if self.descricoes_base:
            melhor, score, _ = process.extractOne(
                desc_norm,
                self.descricoes_base,
                scorer=fuzz.token_sort_ratio,
            )

            if score >= self.SCORE_MINIMO:
                ind = self.mapa_descricao_categoria[melhor]
                cat = self.categorias.get(ind, {})

                return {
                    "IndCategoria": ind,
                    "Categoria": cat.get("Lista"),
                    "Lista": cat.get("Categoria"),
                    "TipoMatch": "FUZZY",
                    "ScoreMatch": score,
                    "DescBase": melhor,
                }

        # 3️⃣ Não classificado
        return {
            "IndCategoria": None,
            "Lista": "0 - Não classificado",
            "Categoria": "Não classificado",
            "TipoMatch": "NÃO CLASSIFICADO",
            "ScoreMatch": None,
            "DescBase": desc_norm,
        }
