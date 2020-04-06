import requests
import time
while(True):
	res = requests.get('http://172.17.0.1:5050/monitoring/updateload')
	time.sleep(5)