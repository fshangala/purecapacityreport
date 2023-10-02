import paramiko
import mailer1

resources=[
  {
    "fqdn":"",
    "username":"",
    "password":"",
    "commands":[]
  },
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
text_data=""
for resource in resources:
  self.ssh.connect(resource["fqdn"], 22, resource["username"], resource["password"], look_for_keys=False)
  text_data += "\n<b>"+resource["fqdn"]+"</b>"
  for command in resource["commands"]:
    stdin, stdout, stderr = self.ssh.exec_command(command)
    text_data += f"\n{stdout.read().decode()}"
    print(stderr.read().decode())

ps1file=mailer1.send_mail(mail_body=text_data,**mailer1.conf)
