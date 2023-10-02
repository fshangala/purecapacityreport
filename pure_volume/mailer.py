import pandas
import os, subprocess
import html
import re
from datetime import datetime

conf = {
  'sender_email':'SACNT782@flex.com',
  'receiver_emails':["corporatestorageadministratorteam@flex.com","jiva.mihailovici@flex.com"],
  'subject':'Storage Capacity Report',
  'smtp_server':'appgw.flex.com'
}

root = os.path.dirname(__file__)

def sendMail(dataframes:list[DataFrame] = []):
  receiver_emails_str = str()
  for email in conf['receiver_emails']:
    receiver_emails_str += f'\"{email}\"' if receiver_emails_str == "" else f',\"{email}\"'
    
  with open(os.path.join(root,'template.html'),'r') as template_file:
    html_template = template_file.read()

  html_tables = str()
  filenames_str = str()
  for dataframe in dataframes:
    filename = os.path.join(root,str(datetime.now())+".csv")
    dataframe.to_csv(filename)
    filenames_str += f'\"{{filename}}\"' if filenames_str == "" else f',\"{{filename}}\"'
    html_tables += f"<div style=\"overflow-x: auto;\">{dataframe.to_html(index=False)}</div>"
  html_template = re.sub('{{tables}}',html_tables,html_template)
  
  with open(os.path.join(root,'template.ps1'),'r') as template_file:
    ps1_template = template_file.read()
  
  ps1_template = re.sub('{{sender_email}}',conf['sender_email'],ps1_template)
  ps1_template = re.sub('{{receiver_emails}}',receiver_emails_str,ps1_template)
  ps1_template = re.sub('{{subject}}',conf['subject'],ps1_template)
  ps1_template = re.sub('{{html}}',html_template,ps1_template)
  ps1_template = re.sub('{{smtp_server}}',conf['smtp_server'],ps1_template)
  
  ps1_script = os.path.join(root,f"{datetime.now().timestamp()}.ps1")
  with open(ps1_script,'w') as ps1_file:
    ps1_file.write(ps1_template)
  
  return ps1_script
