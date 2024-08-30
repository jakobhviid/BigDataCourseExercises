import smtplib
import ssl
from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


@dataclass
class EmailClient:
    email: str
    password: str
    server: str = "smtp.gmail.com"
    port: int = 465

    def create_msg(
        self, receiver_email: str, subject: str, body: str, attachment: Path = None
    ) -> str:

        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        if attachment:
            with open(attachment, "rb") as fh:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(fh.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment.name}",
            )
            message.attach(part)

        return message.as_string()

    def send_msg(self, receiver_email: str, msg: str) -> None:
        # Log in to server using secure context and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, receiver_email, msg)
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print("Email sent successfully")
