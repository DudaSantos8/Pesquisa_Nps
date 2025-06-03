import boto3
import os

def send_email(
    sender,#tp
    recipient,#candidato
    subject,#titulo
    body_text,#subtitulo
    body_html,#corpo da pesquisa
    aws_region='sa-east-1',
    charset='UTF-8'
):
    

    client = boto3.client('ses', 
                      aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                      aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
                      region_name=aws_region)
    # client = boto3.client('ses', region_name=aws_region)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except boto3.ClientError as e:
        return {'status': 'E', 'response': e.response['Error']['Message']}
    else:
        return {'status': 'S', 'response': response['MessageId']}