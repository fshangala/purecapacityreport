import pure, mailer, os

filenames = list()

pure_report = pure.CapacityReport(pure.conf)
if pure_report.filename != None:
    filenames.append(pure_report.filename)
    print("Pure1 Report complete!")
else:
    print("Pure1 Report could not generate!")

#netapp_report = netapp.CapacityReport(**netapp.conf)
#if netapp_report.filename != None:
 #   filenames.append(netapp_report.filename)
  #  print("NetApp Report complete!")
#else:
 #   print("NetApp Report could not generate!")
print(filenames)
if len(filenames) > 0:
    print("Sending generated reports to mail...")
    ps1File = mailer.sendMailP(**mailer.conf, filenames=filenames)
    os.remove(ps1File)
else:
    print("No reports generated!")

print("Done!")
