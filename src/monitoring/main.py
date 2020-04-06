from flask import Flask,render_template
from flask import Flask, flash, request, redirect, render_template, make_response
import urllib.request
import requests   
import os
import codecs
from flask import send_from_directory
app = Flask(__name__)


load = {"ip1:port1":200,"ip2:port2":1000,"ip3:port3":1000};


@app.route("/monitoring/get_load")
def getapps():
    return load



if __name__ == "__main__":        # on running python app.py
    app.run(debug=True,port=5050) 
