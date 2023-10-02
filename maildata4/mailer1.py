import subprocess

import pandas
import os, subprocess
from datetime import datetime

conf = {
    'sender_email':'SACNT782@flex.com',
    'receiver_emails':["corporatestorageadministratorteam@flex.com","jiva.mihailovici@flex.com"],
    'subject':'Storage Capacity Report',
    'smtp_server':'appgw.flex.com'
}

def send_mail(smtp_server:str, sender_email:str, receiver_emails:list, subject:str, mail_body:str):
    receiver_email_str=""
    for receiver_email in receiver_emails:
        if receiver_email_str == "":
            receiver_email_str += f'\"{receiver_email}\"'
        else:
            receiver_email_str += f',\"{receiver_email}\"'
    
    fancy_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
</style>
</head>
<body>
<pre>
{mail_body}
</pre>
</body>
</html>
    """
    
    ps = f"""
$date = get-date
$From = "{sender_email}"
$To = @({receiver_email_str})
$Subject = "{subject}"
$Body = '{fancy_html}'
$SMTPServer = "{smtp_server}"
Send-MailMessage -To $To -From $From -SmtpServer $SMTPServer -Subject $Subject -Body $Body -BodyAsHtml
    """
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(datetime.now().timestamp())+".ps1")
    with open(filepath, "w") as file:
        file.write(ps)
    os.system(f'cmd /c "powershell {filepath}"')
    return filepath