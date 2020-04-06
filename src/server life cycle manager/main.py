from flask import Flask,request
import requests
app = Flask(__name__)

def load_balance():
	return "NO_MACHINE","",""

def allocate_new_machine():
	result,ip,port="","",""
	res = requests.get('http://localhost:6060/service_registry/get_free_list')
	free_list = (res.json())["free"]
	if(len(free_list)==0):
		result = "NO_MACHINE"
	else:
		result = "OK"
		ip = free_list[0].split(":")[0]
		port = free_list[0].split(":")[1]
		requests.get('http://localhost:6060/service_registry/remove_ip_from_freelist/'+ip+"/"+port)
	return result,ip,port


@app.route("/server_lcm/allocate_server")
def allocate_server():
	result,ip,port = load_balance()
	if(result=="NO_MACHINE"):
		result,ip,port = allocate_new_machine()
	return {"result":result,"ip":ip,"port":port}

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=7070) 
