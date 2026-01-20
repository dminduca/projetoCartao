import re
import unicodedata

def normalizar_texto(texto: str) -> str:
    """
    Normaliza textos para comparação e categorização:
    - lowercase
    - remove acentos
    - remove caracteres especiais
    - padroniza espaços
    """
    if not texto:
        return ""

    texto = texto.lower().strip()

    # remove acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    # remove caracteres especiais
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)

    # normaliza espaços
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()
