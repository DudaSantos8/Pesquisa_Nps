import os
import boto3
from logs.logger_config import logger
from botocore.exceptions import ClientError

def send_email(
    sender: str,
    recipient: str,
    subject: str,
    body_text: str,
    body_html: str,
    aws_region: str,
    charset: str
) -> dict:

    from dotenv import load_dotenv
    load_dotenv()

    logger.info("Criando cliente SES")
    logger.info(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
    logger.info(f"AWS_SECRET_ACCESS_KEY: {'✔️' if os.getenv('AWS_SECRET_ACCESS_KEY') else '❌'}")
    logger.info(f"AWS_SESSION_TOKEN: {'✔️' if os.getenv('AWS_SESSION_TOKEN') else '❌'}")

    client = boto3.client("ses",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=aws_region
    )

    try:
        response = client.send_email(
            Destination={"ToAddresses": [recipient]},
            Message={
                "Body": {
                    "Html": {"Charset": charset, "Data": body_html},
                    "Text": {"Charset": charset, "Data": body_text}
                },
                "Subject": {"Charset": charset, "Data": subject}
            },
            Source=sender,
        )
        logger.info("E-mail enviado com sucesso.")
        return {"status": "S", "response": response["MessageId"]}
    except ClientError as e:
        logger.error(f"Erro ao enviar e-mail: {e.response['Error']['Message']}")
        return {"status": "E", "response": e.response["Error"]["Message"]}
