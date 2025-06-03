import csv
import os
from logs.logger_config import logger

CSV_PATH = r"C:\Users\Zupper\Desktop\TTP\pesquisas_de_satisfacao\registro_candidatos\rejeitados.csv"


def save_rejected_to_csv(data: list):
    headers = ["name", "email", "job", "rejected_at", "send_at", "email_enviado"]
    existentes = set()

    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chave = (row["email"], row["rejected_at"])
                existentes.add(chave)

    novos = [row for row in data if (row["email"], row["rejected_at"]) not in existentes]

    if not novos:
        logger.info("Nenhum novo candidato rejeitado para adicionar.")
        return

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if os.stat(CSV_PATH).st_size == 0:
            writer.writeheader()
        for row in novos:
            row["email_enviado"] = False
            writer.writerow(row)

    logger.info(f"{len(novos)} novos registros adicionados ao CSV.")
