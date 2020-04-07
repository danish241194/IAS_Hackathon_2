from flask import Flask,request,jsonify
import random
import json
app = Flask(__name__)


servers = ["127.0.0.1:11000","127.0.0.1:11001","127.0.0.1:11002","127.0.0.1:11003","127.0.0.1:11004"];


@app.route("/monitoring/get_load")
def get_load():
	file=open("output.json","r")
	data=json.load(file)
	return jsonify(data)

# @app.route("/monitoring/updateload")
# def update_load():
#     load["ip1:port1"] =random.randrange(100,1500,10)
#     load["ip2:port2"] =random.randrange(100,1500,10)
#     load["ip3:port3"] =random.randrange(100,1500,10)
#     return "OK"


if __name__ == "__main__":        # on running python app.py
    app.run(host="0.0.0.0",port=5050) 
