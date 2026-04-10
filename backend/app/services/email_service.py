from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
from app.config import settings
from app.models.payment import Payment

env = Environment(loader=FileSystemLoader("app/templates"))


def send_payment_email(payment: Payment, status: str, reason: str | None = None) -> None:
    template = env.get_template("payment_status.html")

    html = template.render(
        name=payment.user.name,
        amount=payment.amount / 100,
        status=status,
        reason=reason,
        payment_id=payment.id,
        gateway=payment.gateway,
    )

    msg = MIMEText(html, "html")
    msg["Subject"] = f"Payment {status}"
    msg["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM_ADDRESS}>"
    msg["To"] = payment.user.email
    msg["Reply-To"] = settings.MAIL_FROM_ADDRESS
    msg["Content-Type"] = "text/html"

    with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
        if settings.MAIL_ENCRYPTION == "tls":
            server.starttls()

        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(msg)
