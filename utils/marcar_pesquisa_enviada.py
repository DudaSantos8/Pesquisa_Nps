import csv
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

def marcar_email_enviado(email: str, rejected_at: str, job: str):
    before_hash = get_file_hash(CSV_PATH)
    linhas = []

    with open(CSV_PATH, mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["email"] == email and row["rejected_at"] == rejected_at and row["job"] == job:
                row["email_enviado"] = "True"
            linhas.append(row)

    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(linhas)

    after_hash = get_file_hash(CSV_PATH)

    if before_hash != after_hash:
        try:
            s3.upload_file(CSV_PATH, S3_BUCKET_NAME, S3_KEY)
            logger.info(f"📤 CSV atualizado enviado para o S3 após edição: s3://{S3_BUCKET_NAME}/{S3_KEY}")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar CSV para o S3: {e}")
    else:
        logger.info("Nenhuma alteração detectada no CSV após marcar email enviado.")
