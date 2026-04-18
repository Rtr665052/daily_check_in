import json
import os
import urllib.parse
import logging
from datetime import datetime
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client("ses")

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]
FORM_URL = os.environ.get("FORM_URL", "")


def lambda_handler(event, context):
    today = datetime.utcnow().date().isoformat()

    token_payload = {
        "person_id": "fiancee",
        "date": today
    }

    token = urllib.parse.quote(json.dumps(token_payload))
    form_link = f"{FORM_URL}?token={token}&date={today}"

    subject = f"Daily Check-In for {today}"

    body_text = f"""Hi,

Here is your daily check-in form for {today}.

Please complete it here:
{form_link}

Love you.
"""

    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2>Daily Check-In</h2>
        <p>Here is your check-in form for <strong>{today}</strong>.</p>
        <p>
          <a href="{form_link}" style="display:inline-block;padding:12px 18px;background:#2563eb;color:#ffffff;text-decoration:none;border-radius:6px;">
            Open Daily Check-In
          </a>
        </p>
        <p>Love you.</p>
      </body>
    </html>
    """

    logger.info("Sending email from %s to %s", SENDER_EMAIL, RECIPIENT_EMAIL)

    response = ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [RECIPIENT_EMAIL]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body_text},
                "Html": {"Data": body_html}
            }
        },
        ConfigurationSetName="daily-checkin-config",
        Tags=[
        {"Name": "MessageTag", "Value": "daily-checkin"}
        ]
    )

    logger.info("SES MessageId: %s", response.get("MessageId"))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Email sent successfully",
            "message_id": response.get("MessageId"),
            "date": today
        })
    }