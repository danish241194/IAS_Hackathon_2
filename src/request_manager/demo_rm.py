import sys
import json
import requests

file=open("demo.json","r")
config_data=json.load(file)

# data={"action":"Start","servicename":"service-4","config":config_data}
data={"action":"None","servicename":"","config":config_data}
# data={"action":"Stop","servicename":"service-4","config":config_data}

print(sys.argv[1])
res = requests.post('http://127.0.0.1:'+str(5053)+'/schedule_service', json=data)

print(res.json())
