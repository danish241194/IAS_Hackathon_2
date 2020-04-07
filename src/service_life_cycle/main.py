from flask import Flask,request
import requests
app = Flask(__name__)


@app.route('/start_stop_service', methods=['GET', 'POST'])
def start_stop_service():
    content = request.json
    print(content)
    return {"result":"OK"}

if __name__ == "__main__":        # on running python app.py
	app.run(debug=True,port=8080) 