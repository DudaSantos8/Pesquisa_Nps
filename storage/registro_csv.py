import csv
import os
import boto3
from utils.hash_util import get_file_hash
from logs.logger_config import logger
import os
from dotenv import load_dotenv

load_dotenv()  # Apenas se estiver usando um arquivo .env

DEFAULT_CSV_PATH = os.path.join(os.getcwd(), "registro_candidatos", "rejeitados.csv")
CSV_PATH = os.getenv("CSV_REJEITADOS_PATH", DEFAULT_CSV_PATH)

S3_BUCKET_NAME = "seu-nome-do-bucket"
S3_KEY = "rejeitados.csv"

s3 = boto3.client("s3")

def save_rejected_to_csv(data: list):
    headers = ["name", "email", "job", "rejected_at", "send_at", "email_enviado"]
    existentes = set()
    novos = []

    before_hash = get_file_hash(CSV_PATH)

    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chave = (row["email"], row["rejected_at"])
                existentes.add(chave)

    novos = [row for row in data if (row["email"], row["rejected_at"]) not in existentes]

    if not novos:
        logger.info("Nenhum novo candidato rejeitado para adicionar.")
    else:
        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if os.stat(CSV_PATH).st_size == 0:
                writer.writeheader()
            for row in novos:
                row["email_enviado"] = False
                writer.writerow(row)
        logger.info(f"{len(novos)} novos registros adicionados ao CSV.")

    after_hash = get_file_hash(CSV_PATH)
    if before_hash != after_hash:
        try:
            s3.upload_file(CSV_PATH, S3_BUCKET_NAME, S3_KEY)
            logger.info(f"📤 CSV atualizado enviado para o S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar CSV para o S3: {e}")
    else:
        logger.info("Nenhuma alteração real detectada no CSV. Upload para o S3 ignorado.")
