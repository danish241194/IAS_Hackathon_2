
import requests
data = {
  "username": "useruniqueid",
  "application_id": "application_id",
  "service_name": "service_name",
  "singleinstance":True,
  "time": {
    "start": [
      "NOW",
    ],
    "end": [
      "01:31",
    ]
  }
}

res = requests.post('http://localhost:9090/schedule_service', json=data)

print(res.json())
