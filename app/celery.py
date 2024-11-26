from celery import shared_task
from celery.contrib.abortable import AbortableTask
from app import db
from app.models import Tasks, User
import smtplib, os, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import current_user
from dotenv import load_dotenv
from app.config import password, sender_email


load_dotenv()

@shared_task(bind=True, base=AbortableTask)
def send_notif(self, tasker, user_id):
    
    tasks = Tasks.query.filter_by(id = tasker).first()
    user = User.query.filter_by(id=user_id).first()
    
    if tasks:
        tasks.completed = True
        title = tasks.title

        smtp_server = "smtp.gmail.com"
        smtp_port = 465

        password = password
        sender_email = sender_email
        receiver_email = user.email

        if not password or not sender_email or not receiver_email:
            print("Environment variables for email are not set properly.")
            return

        subject = f"Hello {user.username}"
        body = f"Your Task: {title} is overdue"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, password)

            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)

            server.quit()

            print("Email sent successfully")
            

        except Exception as e:
            print(f"Failed to send email: {e}")


        db.session.commit()

    if self.is_aborted():
        return 'Task stopped'

    
    