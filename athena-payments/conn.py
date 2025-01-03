from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client, Client
import smtplib

url: str = "https://clvvpgmntfgznsahgrar.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsdnZwZ21udGZnem5zYWhncmFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzNzgzNzcsImV4cCI6MjA0MDk1NDM3N30.mLbfZ0gWMQaQEsswfHkgJ17p7fnYhk0mWYsDJkuf5Qs"
supabase: Client = create_client(url, key)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'venukumarmd03@gmail.com'
SMTP_PASSWORD = 'avbh khcy obhi wwwh'

def send_confirmation_email(email, number_of_tickets, booking_id):

    # Email content
    subject = "Your Booking is Successful - Athena Payments"
    sender_email = SMTP_USERNAME
    receiver_email = email

    # Create the email body
    body = f"""
    Dear Customer,

    Your booking has been successfully completed.

    Number of Tickets: {number_of_tickets}
    Booking ID: {booking_id}

    Thank you for choosing Athena Payments.

    Best Regards,
    Athena Payments Team
    """

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print(f"Email sent successfully to {receiver_email}")

    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {str(e)}")

def add_to_payments(booking_id,  booking_email, amount):
    validity = datetime.today().isoformat()
    supabase.table("payments").insert({"booking-id": booking_id, "validity": validity, "booking-email": booking_email, "amout": amount}).execute()