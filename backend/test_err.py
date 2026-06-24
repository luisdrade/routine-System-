import urllib.request, json, sys
req = urllib.request.Request('http://localhost:8000/api/chat', data=json.dumps({'message':'oi', 'history':[]}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
  res = urllib.request.urlopen(req)
except Exception as e:
  print(e.read().decode())
import urllib.request, json
req = urllib.request.Request('http://localhost:8000/api/chat', data=json.dumps({'message':'oi', 'history':[]}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
 res = urllib.request.urlopen(req)
 print(res.read().decode())
except Exception as e:
 print('ERR:', e.read().decode())
