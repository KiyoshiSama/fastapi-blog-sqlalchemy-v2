from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME", default=""),  # smtp4dev does not require authentication
    MAIL_PASSWORD=config("MAIL_PASSWORD", default=""),  # smtp4dev does not require authentication
    MAIL_FROM=config("MAIL_FROM", default="no-reply@example.com"),  # Default sender address
    MAIL_PORT=config("MAIL_PORT", cast=int, default=25),  # Port used by smtp4dev
    MAIL_SERVER=config("MAIL_SERVER", default="localhost"),  # smtp4dev server
    MAIL_FROM_NAME=config("MAIL_FROM_NAME", default="Your Name"),  # Sender's name
    MAIL_STARTTLS=config("MAIL_STARTTLS", cast=bool, default=False),
    MAIL_SSL_TLS=config("MAIL_SSL_TLS", cast=bool, default=False),
    USE_CREDENTIALS=config("USE_CREDENTIALS", cast=bool, default=False),
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
