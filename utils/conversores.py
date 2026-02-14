import re
from datetime import datetime, date


MESES_PT = {
    "JAN": "01",
    "FEV": "02",
    "MAR": "03",
    "ABR": "04",
    "MAI": "05",
    "JUN": "06",
    "JUL": "07",
    "AGO": "08",
    "SET": "09",
    "OUT": "10",
    "NOV": "11",
    "DEZ": "12",
}


def converter_valor_para_float(valor_str: str) -> float:
    """
    Converte:
        'R$ 1.234,56'
        '1.234,56'
    para:
        1234.56
    """
    try:
        valor_str = (
            valor_str
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
        return float(valor_str)
    except Exception:
        return 0.0


def converter_data_nubank(data_str: str, nome_arquivo: str) -> date:
    """
    Converte '28 AGO' em date(YYYY, 08, 28)
    Ano inferido do nome do arquivo Nubank_YYYY-MM-DD.pdf
    """
    try:
        dia, mes_abrev = data_str.split()
        mes = MESES_PT.get(mes_abrev.upper(), "01")

        m = re.search(r"Nubank_(\d{4})-\d{2}-\d{2}", nome_arquivo)
        ano = int(m.group(1)) if m else datetime.now().year

        return datetime.strptime(
            f"{ano}-{mes}-{dia}",
            "%Y-%m-%d"
        ).date()
    except Exception:
        return date.today()


def converter_data_picpay(data_str: str, nome_arquivo: str) -> date:
    """
    Converte '24/12' em date(YYYY, 12, 24)
    Ano inferido do nome do arquivo PicPay_Fatura_MMYYYY.pdf
    """
    try:
        m = re.search(r"PicPay_Fatura_(\d{2})(\d{4})", nome_arquivo)
        ano = int(m.group(2)) if m else datetime.now().year

        dia, mes = data_str.split("/")

        return datetime.strptime(
            f"{ano}-{mes}-{dia}",
            "%Y-%m-%d"
        ).date()
    except Exception:
        return date.today()

def converter_data_completa(data_str: str) -> date:
    """
    Converte '05 JAN 2026' -> datetime.date(2026, 1, 5)
    """
    partes = data_str.strip().split()

    if len(partes) != 3:
        raise ValueError(f"Formato inválido de data: {data_str}")

    dia = int(partes[0])
    mes_str = partes[1].upper()
    ano = int(partes[2])

    if mes_str not in MESES_PT:
        raise ValueError(f"Mês inválido: {mes_str}")

    mes = int(MESES_PT[mes_str])

    return date(ano, mes, dia)

def converter_datav_picpay(data_str: str) -> date:
    """Converte 'DD-MM-AAAA' em date (consistente com Nubank)."""
    return datetime.strptime(data_str, "%d-%m-%Y").date()

