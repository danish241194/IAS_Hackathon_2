import kafka
import sys, time
import psutil
import subprocess
import json
from random import random
kafka_server = 'localhost:9092'

def getConnectionDetails():
	ip = sys.argv[1]
	port = sys.argv[2]
	uname = sys.argv[3]
	passw = sys.argv[4]

	return ip, port, uname, passw


if __name__  == "__main__":

	
	ip, port, uname, passw = getConnectionDetails()

	producer = kafka.KafkaProducer(bootstrap_servers=[kafka_server])

	while True:
		stats = ip + ' ' + port + ' ' + uname + ' ' + passw + ' '

		cpu = round(100 - psutil.cpu_percent(), 2)
		stats += str(cpu) + ' '

		free_mem = round(100 - psutil.virtual_memory()[2], 2)
		stats += str(free_mem) + ' '

		no_event = 15000
		stats += str(no_event) + ' '

		free_ram = round(psutil.virtual_memory()[4] / 1024 / 1024 / 1024, 2)
		stats += str(free_ram) + ' '

		# out = subprocess.Popen(['cat','/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE)
		# stdout,stderr = out.communicate()
		# temp = int(stdout.decode().rstrip())/1000
		temp = 46.0+5*random()
		stats += str(temp) + ' '

		n_cores = psutil.cpu_count()
		stats += str(n_cores) + ' '

		la = psutil.getloadavg()
		la1 = la[0]
		stats += str(la1) + ' '

		la2 = la[1]
		stats += str(la2) + ' '

		la3 = la[2]
		stats += str(la3) + ' '

		# print(stats)
		
		producer.send('platform_monitor', bytearray(stats,'utf-8'))
		producer.flush()

		time.sleep(2)