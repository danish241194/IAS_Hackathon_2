from flask import Flask,request
import requests
import paramiko
app = Flask(__name__)



def load_balance():
	res=requests.get('http://localhost:5050/monitoring/get_load')
	data=res.json()
	loads=[]

	for i in range(data["n_servers"]):
		if(data["server_load"][i]["load_average_1"]/data["server_load"]["n_cores"] >= 0.8 or data["server_load"][i]["load_average_5"]/data["server_load"]["n_cores"] >= 0.7):
			continue
		coeff1=1/((3/data["server_load"][i]["free_cpu"])+(1/data["server_load"][i]["free_mem"]))
		coeff2=data["server_load"][i]["number_of_events_per_sec"]/10000 + min(2,data["server_load"][i]["free_RAM"])
		coeff3=1 if data["server_load"][i]["temperature"] < 70 else 0

		coeff=coeff1*coeff2*coeff3

		loads.append((coeff,data["server_load"][i]["ip"],data["server_load"][i]["port"]))

	

	return "N_MACHINE","","","",""
def setup_new_machine(ip,username,password):
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=ip,username=username,password=password)
	ftp_client=ssh_client.open_sftp()
	ftp_client.put("code/machineagent.py","machineagent.py");
	ftp_client.close()
	ssh_client.exec_command("python3 machineagent.py")
	ssh_client.close()
def allocate_new_machine():
	result,ip,username,password="","","",""
	res = requests.get('http://localhost:6060/service_registry/get_free_list')
	free_list = (res.json())["free"]
	if(len(free_list)==0):
		result = "NO_MACHINE"
	else:
		result = "OK"
		ip = free_list[0].split(":")[0]
		username = free_list[0].split(":")[1]
		password = free_list[0].split(":")[2]
		port = free_list[0].split(":")[3]
		requests.get('http://localhost:6060/service_registry/remove_ip_from_freelist/'+ip+"/"+username+"/"+password+"/"+port)
		setup_new_machine(ip,username,password)
	return result,ip,username,password,port


@app.route("/server_lcm/allocate_server")
def allocate_server():
	result,ip,username,password,port = load_balance()
	if(result=="NO_MACHINE"):
		result,ip,username,password,port = allocate_new_machine()
	return {"result":result,"ip":ip,"username":username,"password":password,"port":port}

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=7070) 
