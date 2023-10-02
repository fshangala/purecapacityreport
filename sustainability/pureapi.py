import requests

id_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwdXJlMTphcGlrZXk6S0RhNHRFSzhHSVZ0aUxFUyIsImlhdCI6MTY2MjczNjYxMywiZXhwIjoxNzI1ODk0ODAwfQ.GtpA5KQlO9d10Sv72jlsS655yoe9PW1S4V_pE1bs0U8TFoxLolcG8KREH3x3NJDJkUrF8oPCJGBQQd-gMZjxOBwNGl5sgRPqjLUwjHUDfFXZtyQsURMoNp6W5cR7M2g8RywCTRfxroS-b9EqZ5VhNpNtj_d6VLQN3sauvSkLbM5R0LraPNe37r7utexqce23xaQzfuCI0Z45zsRSi3tnVYJt-gSudP4h-DpqH8trCBPHIVQDkOsgtrg0kaeh0Ay5OfsJvZ_cEDa8zWUph933WN2c7uhkG-ohb6fbSxYCJyGVsBXWPhZwVoN8hbIgeQ0bT51T1V1HRObME83-w3fc9g"
base_url = "" # api server

# Get access token
payload = {
  'grant_type':'urn:ietf:params:oauth:grant-type:token-exchange',
  'subject_token':id_token,
  'subject_token_type':'urn:ietf:params:oauth:token-type:jwt'
}
response = requests.post(f"{base_url}/oauth2/1.0/token",data=payload)

if(response.status_code == 200):
  access_token = response.json()["access_token"]
  
  # Get sustainability arrays
  headers = {
    'Authorization':access_token,
  }
  query = {
    'fqdns':[] # list of array fqdn
  }
  response = requests.get(f"{base_url}/api/1.latest/assessment/sustainability/arrays",headers=headers,params=query)
  print(response.json())
  
  
