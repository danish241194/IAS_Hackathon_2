import sys
import json
import requests
# data = {
# "Application":{
#         "username":"useruniqueid",
#         "application_id":"application_id",
#         "services":{
         
#           "service-5":{
#                 "service_name":"service_name",
#                 "filename":"hello4.py",
#                 "singleinstance":False,
#                 "environment":{
#                     "python3":True,
#                     "tomcat":True,
#                     "java":True,
#                     "c++":False,
#                     "nginx":False,
#                     "python-kafka":True,
#                     "flask":True
#                 },
#                 "time":{
#                     "start":[
#                         "NOW",
                        
#                     ],
#                     "end":[
#                         "20:55"
#                     ]
#                 },
#                 "period":{
#                     "interval":3,
#                     "length":2
#                 },           
#                 "dependency":[],

#                 "sensor":{
#                     "sensor1":{
#                         "sensor_name":"Fan",
#                         "sensor_address":{
#                             "area":"A",
#                             "building":"B",
#                             "room_no":"C"
#                         },
#                         "processing":{
#                             "data_rate":5
#                         }
#                     },
#                     "sensor2":{
#                         "sensor_name":"Lamp",
#                         "sensor_address":{
#                             "area":"A",
#                             "building":"C",
#                             "room_no":"D"
#                         },
#                         "processing":{
#                             "data_rate":1
#                         }
#                     }
#                 }
#             }
#           }
#         }
# }

file=open("user_config.json","r")
config_data=json.load(file)

# data={"action":"Start","servicename":"service-4","config":config_data}
data={"action":"None","servicename":"","config":config_data}
# data={"action":"Stop","servicename":"service-4","config":config_data}

print(sys.argv[1])
res = requests.post('http://localhost:'+str(sys.argv[1])+'/schedule_service', json=data)

print(res.json())
