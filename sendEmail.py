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
                <td style="border:1px solid black;padding:5px;">{arr[x][2]}</td>
                <td style="border:1px solid black;padding:5px;background:lime">{arr[x][3]}</td>
                <td style="border:1px solid black;padding:5px;background:red">{arr[x][4]}</td>
            </tr>"""

    message = f'''<div style="text-align:center;width:100%;font-family:sans-serif;">
                <h1 style="text-align:center;">Du3aaAPI</h1>
                <p style="text-align:center;">postAll function feedback {Date}</p>
                <div style="width:100%">
                    <table style="border:1px solid black;border-collapse:collapse;margin-left:auto;margin-right:auto;text-align:center;">
                        <thead>
                            <tr>
                                <th style="border:1px solid black;padding:5px;">Date</th>
                                <th style="border:1px solid black;padding:5px;">Success</th>
                                <th style="border:1px solid black;padding:5px;">Fail</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tableBody}
                        </tbody>
                    </table>
                </div>
            </div>'''

    msg['From'] = f'Du3aaAPI Monitor <{MY_ADDRESS}>'
    msg['To'] = MY_ADDRESS
    msg['Subject'] = "Post All"
    
    msg.attach(MIMEText(message, 'html'))
    
    s.send_message(msg)
    del msg
        
    s.quit()
