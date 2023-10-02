$date = get-date
$From = "{{sender_email}}"
$To = @({{receiver_emails}})
$Subject = "{{subject}}"
$Body = '{{html}}'
$SMTPServer = "{{smtp_server}}"
Send-MailMessage -To $To -From $From -SmtpServer $SMTPServer -Subject $Subject -Body $Body -BodyAsHtml