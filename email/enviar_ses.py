import os
import boto3
from logs.logger_config import logger
from botocore.exceptions import ClientError
from utils.marcar_pesquisa_enviada import marcar_email_enviado

def send_email(
    sender: str,
    recipient: str,
    job: str,
    rejected_at: str,
    subject: str,
    body_text: str,
    body_html: str,
    aws_region: str,
    charset: str
) -> dict:
    
    logger.info("Criando cliente ses")
    
    from dotenv import load_dotenv
    load_dotenv()
    logger.info(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
    logger.info(f"AWS_SECRET_ACCESS_KEY: {'✔️' if os.getenv('AWS_SECRET_ACCESS_KEY') else '❌'}")
    logger.info(f"AWS_SESSION_TOKEN: {'✔️' if os.getenv('AWS_SESSION_TOKEN') else '❌'}")

    client = boto3.client("ses",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=aws_region
    )
    #client = boto3.client('ses', region_name=aws_region)
    try:
        response = client.send_email(
            Destination={
                "ToAddresses": [recipient],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": charset,
                        "Data": body_html,
                    },
                    "Text": {
                        "Charset": charset,
                        "Data": body_text,
                    },
                },
                "Subject": {
                    "Charset": charset,
                    "Data": subject,
                },
            },
            Source=sender,
        )
    except ClientError as e:
        # Se der erro no SES, apenas loga e devolve status="E"
        logger.error(f"Erro ao enviar e-mail: {e.response['Error']['Message']}")
        return {"status": "E", "response": e.response["Error"]["Message"]}
    else:
        # Se chegou aqui, deu sucesso
        logger.info("E-mail enviado com sucesso, marcando CSV...")
        try:
            marcar_email_enviado(recipient, rejected_at, job)
            logger.info(f"CSV atualizado: email_enviado=True para {recipient}/{rejected_at}")
        except Exception as e_csv:
            # Caso algo dê errado ao atualizar o CSV, você pode logar o erro, mas o e-mail já foi enviado.
            logger.error(f"Falha ao atualizar CSV para {recipient}/{rejected_at}: {e_csv}")
        return {"status": "S", "response": response["MessageId"]}
