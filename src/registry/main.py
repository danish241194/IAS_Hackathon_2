from flask import Flask,request
import random 
app = Flask(__name__)

free_list = ["172.17.0.3:root:pppppp:22","172.17.0.33:root:pppppp:22","172.17.0.44:root:pppppp:22","172.17.0.1:root:pppppp:22"];
service_registry = {"monitoring":"localhost:5050"};

@app.route("/service_registry/get_free_list")
def get_free_list():
    if len(free_list)==0:
        return {"free":"NO_MACHINE"}
    item=[free_list[0]]
    print("item is")
    print(item)
    remove_kernel(item[0].split(":")[0],item[0].split(":")[1],item[0].split(":")[2],item[0].split(":")[3])
    return {"free":item}

@app.route("/service_registry/get_service_location/<service>")
def get_service_location(service):
    return {"location":service_registry[service]};

def remove_kernel(ip,username,password,port):
	free_list.remove(str(ip)+":"+str(username)+":"+str(password)+":"+str(port));



if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=6060) 
