import mailer, os

filenames = [
  "sample.csv"
]

print(filenames)
if len(filenames) > 0:
    print("Sending reports to mail...")
    ps1File = mailer.sendMailP(**mailer.conf, filenames=filenames)
    os.remove(ps1File)
else:
    print("No reports!")

print("Done!")
