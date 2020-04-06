from flask import Flask,request
import random 
app = Flask(__name__)

free_list = ["172.17.0.3:root:pppppp","172.17.0.33:root:pppppp","172.17.0.44:root:pppppp","172.17.0.1:root:pppppp"];
service_registry = {"monitoring":"localhost:5050"};

@app.route("/service_registry/get_free_list")
def get_free_list():
    return {"free":free_list}
@app.route("/service_registry/get_service_location/<service>")
def get_service_location(service):
    return {"location":service_registry[service]};


@app.route("/service_registry/remove_ip_from_freelist/<ip>/<username>/<password>")
def remove_ip_from_freelist(ip,username,password):
    free_list.remove(str(ip)+":"+str(username)+":"+str(password));
    return "OK"


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=6060) 
