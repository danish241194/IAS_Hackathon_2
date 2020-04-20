from flask import Flask,request,Response
import requests
import json
app = Flask(__name__)


# @app.route('/start_stop_service', methods=['GET', 'POST'])
# def start_stop_service():
#     content = request.json
#     print(content)
#     return {"result":"OK"}

@app.route('/make_request/<i>')
def start_stop_service(i):
    # i="jay_krishna"
    r=requests.get(url="http://127.0.0.1:5054/serverlcm/allocate_server/"+i)
    return r.json()

@app.route("/servicelcm/service/update",methods=['POST'])
def receive():
	data=request.get_json()
	print(data)

	data={"status":"ok"}
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	# print(resp.json)
	return resp

@app.route('/servicelcm/service/topology/<username>')
def process(username):
	file=open("meta.json")
	data=json.load(file)
	send_data=None

	for _ in data:
		if(_["serviceName"]==username):
			send_data=_
			break
	return json.dumps([send_data])


if __name__ == "__main__":        # on running python app.py
	app.run(debug=True,port=8080) 