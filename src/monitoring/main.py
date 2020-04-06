from flask import Flask,request
import random 
app = Flask(__name__)


load = {"ip1:port1":200,"ip2:port2":1000,"ip3:port3":1000};


@app.route("/monitoring/get_load")
def get_load():
    return load


@app.route("/monitoring/updateload")
def update_load():
    load["ip1:port1"] =random.randrange(100,1500,10)
    load["ip2:port2"] =random.randrange(100,1500,10)
    load["ip3:port3"] =random.randrange(100,1500,10)
    return "OK"


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=5050) 
