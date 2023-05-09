from email import message
import smtplib
from email.mime.text import MIMEText

# Here I defined the email logic for sending emails to the customer and the dealer when a new feedback is submitted.


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '010134d040efaa'
    password = '5e47167de70813'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

# Here I collect the senders and recipients for the customer and the dealer when a new feedback is submitted
    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

   # Try to send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        # If an error occurs, print it out
        print(f"Error: {e}")
