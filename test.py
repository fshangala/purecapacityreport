import pandas
import numpy

report = [
  "Array",
  "Physical Raw Capacity (TB)",
  "Usable Raw Capacity (TB)",
  "Utilized on Raw (TB)",
  "Efficiency (Data Reduction)",
  "Array Load",
  "Vendor",
  "Model"
]
initData = [0 for x in range(len(report))]
body = numpy.array([initData for x in range(len(report))])

df = pandas.DataFrame(data=body,columns=report)
df.to_csv("sample.csv",index=False)