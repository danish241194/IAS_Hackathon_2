from flask import Flask,request
import random 
app = Flask(__name__)

free_list = ["ip4:port4","ip5:port5","ip6:port7","ip7:port7"];
service_registry = {"monitoring":"localhost:5050"};

@app.route("/service_registry/get_free_list")
def get_free_list():
    return {"free":free_list}
@app.route("/service_registry/get_service_location/<service>")
def get_service_location(service):
    return {"location":service_registry[service]};


@app.route("/service_registry/remove_ip_from_freelist/<ip>/<port>")
def remove_ip_from_freelist(ip,port):
    free_list.remove(str(ip)+":"+str(port));
    return "OK"


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=6060) 
