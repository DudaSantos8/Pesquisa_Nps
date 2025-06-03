from datetime import date
import os
import csv
from logs.logger_config import logger

CSV_PATH = r"C:\Users\Zupper\Desktop\TTP\pesquisas_de_satisfacao\registro_candidatos\rejeitados.csv"

def buscar_envios_hoje() -> list:
    hoje = date.today().isoformat()
    encontrados = []

    if not os.path.exists(CSV_PATH):
        logger.warning("Arquivo CSV não encontrado.")
        return []

    with open(CSV_PATH, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("send_at") == hoje:
                encontrados.append(row)

    logger.info(f"{len(encontrados)} candidatos encontrados com envio marcado para hoje.")
    return encontrados
