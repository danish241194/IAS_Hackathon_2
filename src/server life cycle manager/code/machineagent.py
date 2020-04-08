import requests
import sys
a=1
import time
while True:
	data = {"ip":sys.argv[1],"number":a}
	a+=1
	res = requests.post('http://172.17.0.1:5050/monitoring/update', json=data)
	time.sleep(5)
