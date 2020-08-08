import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

def sendEmail(success, failed):
    MY_ADDRESS = os.environ.get('EMAIL_USER')
    PASSWORD = os.environ.get('EMAIL_PASS')

    now = datetime.now()
    Time=now.strftime("%I:%M %p")
    Date=now.strftime("%F")

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = f'''<p>Du3aaAPI PostAll info {Date}</p>
    <table style="border-collapse: collapse;border: 1px solid black;">
        <thead>
            <tr>
                <th style="border: 1px solid black;">Date</th>
                <th style="border: 1px solid black;">Success</th>
                <th style="border: 1px solid black;">Failed</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid black;text-align: center;">{Time}</td>
                <td style="border: 1px solid black;text-align: center; background-color: lime;">{success}</td>
                <td style="border: 1px solid black;text-align: center; background-color: red;">{failed}</td>
            </tr>
        </tbody>
    </table>'''

    msg['From'] = f'Du3aaAPI Monitor <{MY_ADDRESS}>'
    msg['To'] = MY_ADDRESS
    msg['Subject'] = "Post All"
    
    msg.attach(MIMEText(message, 'html'))
    
    s.send_message(msg)
    del msg
        
    s.quit()
    
if __name__ == '__main__':
    sendEmail(1, 2)
