from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

# load_dotenv(".env")


class Envs:
    MAIL_USERNAME = ""  # smtp4dev does not require authentication
    MAIL_PASSWORD = ""  # smtp4dev does not require authentication
    MAIL_FROM = "no-reply@example.com"  # Default sender address
    MAIL_PORT = 25  # Port used by smtp4dev
    MAIL_SERVER = "localhost"  # smtp4dev server
    MAIL_FROM_NAME = "Your Name"


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    TEMPLATE_FOLDER="app/templates/email",
)


async def send_email_async(subject: str, email_to: str, body: dict):

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name="email.html")
        print({"details": "code sent"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def send_email_background(
    background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")


