import http.client
import mimetypes
import base64
import json

#create the Base64 encoded basic authorization string
clientID="0581f3f6488cadd6a9639c768f90b5c5"
clientsecret="J3HFv9HzMcmDYCMp9h6Epvu2LjUQKKLihYPkcsCZYzWABOFCxhzil6QaLqKvexX2"
auth = f"{clientID}:{clientsecret}"
encodedBytes=base64.b64encode(auth.encode("utf-8"))
authStr = str(encodedBytes, "utf-8")

#create the connection
conn = http.client.HTTPSConnection("iad1.qualtrics.com")
body = "grant_type=client_credentials&scope=manage:all"
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
headers['Authorization'] = f'Basic {authStr}'

#make the request
conn.request("POST", "/oauth2/token", body, headers)
res = conn.getresponse()
data = res.read()
values = json.loads(data.decode("utf-8"))
print(values)

# create the request
body = ''
headers = {
  'Authorization': f'Bearer {values["access_token"]}'
}

# make the request
conn.request("GET", "/API/v3/whoami", body, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
