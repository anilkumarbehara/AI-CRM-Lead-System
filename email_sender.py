import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, ReplyTo
from supabase_db import insert_message

def send_email(to_email, subject, body, lead_id=None):
    reply_to_email = f"lead-{lead_id}@reply.aicrmflow.tech" if lead_id else "sales@aicrmflow.tech"

    message = Mail(
        from_email=Email("sales@aicrmflow.tech"),
        to_emails=To(to_email),
        subject=subject,
        plain_text_content=Content("text/plain", body),
    )
    message.reply_to = ReplyTo(reply_to_email)

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    response = sg.send(message)

    print("SENDGRID STATUS:", response.status_code)
    print("REPLY TO USED:", reply_to_email)

    if lead_id is not None:
        insert_message({
            "lead_id": lead_id,
            "direction": "outbound",
            "subject": subject,
            "body": body,
            "sender_email": "sales@aicrmflow.tech",
            "thread_key": f"lead-{lead_id}",
        }) 