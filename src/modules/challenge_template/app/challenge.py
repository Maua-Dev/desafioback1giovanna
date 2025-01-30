import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def lambda_handler():
    s3 = boto3.client('s3', region_name='sa-east-1')

    BUCKET_NAME = "challenge-storage-devcommunitymaua"
    OBJECT_KEY = "kick buttowski.png"

    # Buscando a imagem no S3
    img_obj = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
    img_bytes = img_obj["Body"].read()

    # Criando o e-mail
    message = MIMEMultipart()
    message["Subject"] = "Desenho Perdido de Charles"
    message["From"] = "contato@devmaua.com"
    message["To"] = "gio.oliver.albuquerque@gmail.com"

    # Anexando a imagem
    mime_base = MIMEBase("image", "png")
    mime_base.set_payload(img_bytes)
    encoders.encode_base64(mime_base)
    mime_base.add_header("Content-Disposition", f'attachment; filename="{OBJECT_KEY}"')
    message.attach(mime_base)

    # Enviando o e-mail pelo SES
    ses = boto3.client('ses', region_name='sa-east-1')

    response = ses.send_raw_email(
        Source="contato@devmaua.com",
        Destinations=["gio.oliver.albuquerque@gmail.com","22.01082-3@maua.br"],
        RawMessage={"Data": message.as_string()}
    )

    return {
        "statusCode": 200,
        "body": "E-mail enviado com sucesso!",
        "response": response
    }

lambda_handler()