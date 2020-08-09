import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

def sendEmail(arr):
    MY_ADDRESS = os.environ.get('EMAIL_USER')
    PASSWORD = os.environ.get('EMAIL_PASS')

    now = datetime.now()
    Date=now.strftime("%F")

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    tableBody = ''

    for x in range(len(arr)):
        tableBody += f"""
            <tr>
                <td style="border: 1px solid black;text-align: center;">{arr[x][2]}</td>
                <td style="border: 1px solid black;text-align: center; background-color: lime;">{arr[x][3]}</td>
                <td style="border: 1px solid black;text-align: center; background-color: red;">{arr[x][4]}</td>
            </tr>"""

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
            {tableBody}
        </tbody>
    </table>'''

    msg['From'] = f'Du3aaAPI Monitor <{MY_ADDRESS}>'
    msg['To'] = MY_ADDRESS
    msg['Subject'] = "Post All"
    
    msg.attach(MIMEText(message, 'html'))
    
    s.send_message(msg)
    del msg
        
    s.quit()
