from flask import Flask,request,Response
import requests
import json
import threading
import paramiko
app = Flask(__name__)

testing_new_machine  = False
lock_load = threading.Lock()
lock_allocate = threading.Lock()

def load_balance():
	lock_load.acquire()
	res=requests.get('http://localhost:5050/monitoring/get_load')
	data=res.json()
	loads=[]

	for i in range(data["n_servers"]):
		if(data["server_load"][i]["load_average_1"]/data["server_load"][i]["n_cores"] >= 0.8 or data["server_load"][i]["load_average_5"]/data["server_load"][i]["n_cores"] >= 0.7):
			continue
		coeff1=1/((3/data["server_load"][i]["free_cpu"])+(1/data["server_load"][i]["free_mem"]))
		coeff2=data["server_load"][i]["number_of_events_per_sec"]/10000 + min(2,data["server_load"][i]["free_RAM"])
		coeff3=1 if data["server_load"][i]["temperature"] < 70 else 0

		coeff=coeff1*coeff2*coeff3

		loads.append((coeff,data["server_load"][i]["ip"],data["server_load"][i]["port"],data["server_load"][i]["username"],data["server_load"][i]["password"]))

	if(len(loads)==0):
		lock_load.release()
		return "NO MACHINE","","","",""
	else:
		# print(loads)
		loads.sort(key = lambda x:x[0],reverse=True)
		# print(loads)
		lock_load.release()
		return "OK",loads[0][1],loads[0][3],loads[0][4],loads[0][2]

def setup_new_machine(ip,username,password,port):
	print("setup_new_machine")
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=ip,username=username,password=password)
	ftp_client=ssh_client.open_sftp()
	ftp_client.put("code/machineagent.py","machineagent.py");
	ftp_client.close()
	ssh_client.exec_command("python3 machineagent.py "+str(ip)+" "+port+" "+username+" "+password)
	ssh_client.close()
	
def allocate_new_machine():
	lock_allocate.acquire()
	result,ip,username,password="","","",""
	res = requests.get('http://localhost:6060/service_registry/get_free_list')
	free_list = (res.json())["free"]
	if( len(free_list)==0):
		result = "NO MACHINE"
	else:
		result = "OK"
		ip = free_list[0].split(":")[0]
		username = free_list[0].split(":")[1]
		password = free_list[0].split(":")[2]
		port = free_list[0].split(":")[3]
		setup_new_machine(ip,username,password,port)

	lock_allocate.release()
	return result,ip,username,password,port

def allocate_server_kernel(serviceid):
	global testing_new_machine
	result,ip,username,password,port = load_balance()
	# print("Result: {}".format(result))
	if(testing_new_machine or result=="NO MACHINE"):
		print("allocate new machine")
		result,ip,username,password,port = allocate_new_machine()

	data={"result":result,"serviceid": serviceid,"serverip":ip,"machineusername":username,"password":password,"sshPort":port}

	r=requests.post(url="http://127.0.0.1:8080/servicelcm/service/update",json=data)
	print(r.json())


@app.route("/serverlcm/allocate_server/<serviceid>")
def allocate_server(serviceid):
	_=threading.Thread(target=allocate_server_kernel,args=(serviceid,))
	_.start()

	data={"status":"ok"}
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=7070) 
