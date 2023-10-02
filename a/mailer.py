import pandas
import os, subprocess

conf = {
    'sender_email':'SACNT782@flex.com',
    'receiver_emails':["corporatestorageadministratorteam@flex.com","jiva.mihailovici@flex.com"],
    'subject':'Storage Capacity Report',
    'smtp_server':'appgw.flex.com'
}

def sendMailP(sender_email:str, receiver_emails:list, subject:str, smtp_server:str, filenames:list):
    basepath = os.path.abspath(os.path.dirname(__file__))
    #csvpath = os.path.join(basepath, filename+"_report.csv")
    
    HTMLtables = ""
    for filename in filenames:
        headers = [*pandas.read_csv(os.path.join(os.path.dirname(__file__), filename+"_report.csv"), nrows=1)]
        if filename[0]=="N":
            pd = pandas.read_csv(os.path.join(os.path.dirname(__file__), filename+"_report.csv"), usecols=[c for c in headers[1:]])
        else :
            pd = pandas.read_csv(os.path.join(os.path.dirname(__file__), filename+"_report.csv"), usecols=[c for c in headers])
        HTMLtables += f"<br/>{pd.to_html()}"

    filenames_str=""
    for filename in filenames:
        if filenames_str == "":
            filenames_str += f'\"{os.path.join(basepath, filename+"_report.csv")}\"'
        else:
            filenames_str += f',\"{os.path.join(basepath, filename+"_report.csv")}\"'

    receiver_email_str=""
    for receiver_email in receiver_emails:
        if receiver_email_str == "":
            receiver_email_str += f'\"{receiver_email}\"'
        else:
            receiver_email_str += f',\"{receiver_email}\"'

    fancy_html = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
font-family: Arial, Helvetica, sans-serif;
border-collapse: collapse;
width: 100%;
}

table td, table th {
border: 1px solid black;
}

table tr:nth-child(even){background-color: #f2f2f2;}

table tr:hover {background-color: #ddd;}

table th {
text-align: center;
background-color: lightblue;
color: black;
}
</style>
</head>
<body>
    """

    fancy_html += f"{HTMLtables}"
    fancy_html += """

    <br>
<pre>
<small>
Usable Space (TB)         - Total usable storage occupied by data and metadata
Data Reduction (Unit)     - Ratio of mapped sectors within a volume versus the amount of physical space the data occupies after data compression and deduplication. 
                             The data reduction ratio does not include thin provisioning savings
Effective Capacity (TB)   - Usable space(TB) * Expected Data Reduction; expected Data Reduction: FlashArray savings = 4; FlashBlade = 1
Over prov (%)             - More storage space may be allocated than is available on the storage (%)
Allocated Space (TB)      - Over Prov ( %) * Usable space (TB)
Used Space (TB)           - Physical storage space occupied by volume, snapshot, shared space, and system data
Provisioned Space (%)     - The total provisioned storage space on the Pure Storage FlashArray volume. Allocated Space (TB) / Effective Capacity (TB)*100
Space Used (%)            - Physical storage space occupied by volume, snapshot, shared space, and system data
Snapshot (TB)             - Physical space occupied by data unique to one or more snapshots
Snapshot Used (%)         - Used space on the storage array in (%)
Array Load                - Average Load on that storage; an overall parameter that consider, IOPS, response time, controller resource utilization.
</small>
</pre>


</body>
</html>
    """
    ps = f"""
$date = get-date
$From = "{sender_email}"
$To = @({receiver_email_str})
$Attachment = @({filenames_str})
$Subject = "{subject}"
$Body = "$date - Pure and Netapp Capacity report"
$Body += '{fancy_html}'
$SMTPServer = "{smtp_server}"
Send-MailMessage -To $To -From $From -SmtpServer $SMTPServer -Subject $Subject -Body $Body -Attachments $Attachment -BodyAsHtml
    """
    with open(os.path.join(os.path.dirname(__file__), filename+".ps1"), "w") as file:
        file.write(ps)
    
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename+".ps1")
    print(filepath)
    #result = subprocess.check_output([powershell, f"\"{filepath}\""])
    #print(result.decode("utf-8"))
    os.system(f'cmd /c "powershell {filepath}"')
    return filepath