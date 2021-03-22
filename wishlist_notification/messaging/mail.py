"""
mail.py
===========
Util for sending emails and attachments through smtp.
"""

from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import unicodedata
from config import SMTP_SERVER_PORT, SMTP_SERVER


def send_email(
    sender,
    to=None,
    subject="",
    body="",
    cc=None,
    bcc=None,
    attachments=None,
    as_html=False,
    encoding="utf-8",
):
    """Send email through smtp. Body of email defaults to html.

    Args:
        sender (str): Email address of sender
        to (str, [str]): Email address of recipients
        subject (str): Subject of the email
        body (str): Body of the email
        cc (str, [str]): Email address of CC
        bcc (str, [str]): Email address of BCC
        attachments ([(str, bytes), ...]): List of tuple (filename, content), where content is an array of bytes of the
            file
        as_html (bool): Convert body in Html
        encoding (str): Encoding to use. Defaults to "latin1" which supports French accents
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["Subject"] = subject

    if to is not None:
        if isinstance(to, list) and len(to) > 1:
            msg["To"] = ", ".join(sanitize(to))
        else:
            msg["To"] = sanitize(to)

    if cc is not None:
        if isinstance(cc, list) and len(cc) > 1:
            msg["Cc"] = ", ".join(sanitize(cc))
        else:
            msg["Cc"] = sanitize(cc)

    if bcc is not None:
        if isinstance(cc, list) and len(bcc) > 1:
            msg["Bcc"] = ", ".join(sanitize(bcc))
        else:
            msg["Bcc"] = sanitize(bcc)

    if as_html:
        msg.attach(MIMEText(body, "html", _charset=encoding))
    else:
        msg.attach(MIMEText(body, "plain", _charset=encoding))

    attachments = attachments or []
    for filename, content in attachments:
        part = MIMEApplication(content, Name=filename)
        part["Content-Disposition"] = 'attachment; filename="%s"' % filename
        msg.attach(part)

    s = smtplib.SMTP(SMTP_SERVER, port=SMTP_SERVER_PORT)
    s.send_message(msg)


def sanitize(input_str):
    """Removes accents and puts everything in lowercase, Accepts input in string or as list
    Source: https://stackoverflow.com/a/517974/152244

    Args:
        input_str (str or list): String or list of strings that you want to modify
    """

    # Convert from list to string
    if type(input_str) is list:
        input_str = ", ".join(input_str)

    input_str = input_str.lower()
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    sanitized_form = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    # Convert back to list if list was received as input
    if ", " in sanitized_form:
        sanitized_form = sanitized_form.split(", ")

    return sanitized_form
