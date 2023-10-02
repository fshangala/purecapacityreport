from pypureclient import pure1
import datetime
import mailer
import os
import pandas

conf = {
  "app_id":"pure1:apikey:KDa4tEK8GIVtiLES",
  "id_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwdXJlMTphcGlrZXk6S0RhNHRFSzhHSVZ0aUxFUyIsImlhdCI6MTY2MjczNjYxMywiZXhwIjoxNzI1ODk0ODAwfQ.GtpA5KQlO9d10Sv72jlsS655yoe9PW1S4V_pE1bs0U8TFoxLolcG8KREH3x3NJDJkUrF8oPCJGBQQd-gMZjxOBwNGl5sgRPqjLUwjHUDfFXZtyQsURMoNp6W5cR7M2g8RywCTRfxroS-b9EqZ5VhNpNtj_d6VLQN3sauvSkLbM5R0LraPNe37r7utexqce23xaQzfuCI0Z45zsRSi3tnVYJt-gSudP4h-DpqH8trCBPHIVQDkOsgtrg0kaeh0Ay5OfsJvZ_cEDa8zWUph933WN2c7uhkG-ohb6fbSxYCJyGVsBXWPhZwVoN8hbIgeQ0bT51T1V1HRObME83-w3fc9g",
  "volume_names":['DUCSA009-F301-PURE-FC-T1-V001', 'DUCSA008-F601-PURE-FC-T1-V001'],
  "volume_metrics_names":["volume_provisioned_capacity","volume_data_reduction","volume_physical_capacity","volume_snapshots_physical_capacity","volume_virtual_capacity","volume_snapshots_virtual_capacity"],
  "time_offset":24,
  "byte_multiple":1099511627776
}

root = os.path.dirname(__file__)

def unix_time_millis(dt):
  epoch = datetime.datetime.utcfromtimestamp(0)
  return int((dt - epoch).total_seconds() * 1000)

start_time = unix_time_millis(datetime.datetime.now() - datetime.timedelta(hours=conf["time_offset"]))
end_time= unix_time_millis(datetime.datetime.now())
print(root, "Configured.")

# create connection
client = pure1.Client(app_id=conf["app_id"],id_token=conf["id_token"])
print(conf["app_id"], "Connection established.")

# get volumes
response = client.get_volumes(names=conf["volume_names"])
volumes = list(response.items)
print(len(volumes),"Volumes collected.")

# get volume metrix and save to csv file
metrics = list()
for volume in volumes:
  response = client.get_metrics_history(aggregation='avg',names=conf["volume_metrics_names"],resource_ids=volume.id, resolution=86400000, start_time=start_time, end_time=end_time)
  volume_metrics = list(response.items)
  metrics.append({'volume':volume,'metrics':volume_metrics})
print(len(metrics),"Volume metrics collected.")

# prepare data
print('Preparing collected data...')
data = {'array':pandas.Series([]),'volume':pandas.Series([])}

for n in conf['volume_metrics_names']:
  data[n] = pandas.Series([])
  
for m in metrics:
  data["array"]=data["array"].append(pandas.Series([m['volume'].arrays[0].name]))
  data["volume"]=data["volume"].append(pandas.Series([m['volume'].name]))
  for metric in m['metrics']:
    data[metric.name]=data[metric.name].append(pandas.Series([metric.data[1][1]]))

# generate dataframe
print("Generating dataframe...")
df = pandas.DataFrame(data)

# clean data
def KB_to_GB(x):
  return x/(1024**3)

def GB_to_TB(x):
  return x/1024

def Round_Off(x):
  return round(x,2)

def Add_GB_Label(x):
  return str(x)+"GB"

def Add_TB_Label(x):
  return str(x)+"TB"

for m in conf['volume_metrics_names']:
  if not m == 'volume_data_reduction':
    df[m]=df[m].apply(KB_to_GB)
    if not m == 'volume_snapshots_physical_capacity':
      df[m]=df[m].apply(GB_to_TB)
      df[m]=df[m].apply(Round_Off)
      df[m]=df[m].apply(Add_TB_Label)
    else:
      df[m]=df[m].apply(Round_Off)
      df[m]=df[m].apply(Add_GB_Label)
  
print(df)
mailer.sendMail([df])