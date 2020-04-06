from flask import Flask,request
import random 
app = Flask(__name__)


load = {"ip1:username1:password1":200,"ip2:username2:password2":1000,"ip3:username3:password3":1000};


@app.route("/monitoring/get_load")
def get_load():
    return load


@app.route("/monitoring/updateload")
def update_load():
    load["ip1:username1:password1"] =random.randrange(100,1500,10)
    load["ip2:username2:password2"] =random.randrange(100,1500,10)
    load["ip3:username3:password3"] =random.randrange(100,1500,10)
    return "OK"


if __name__ == "__main__":        # on running python app.py
    app.run(host="0.0.0.0",port=5050) 
