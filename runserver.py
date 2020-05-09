"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template
from BiVOsendRequest import app
from pymongo import MongoClient
import json
import socket

client = MongoClient("mongodb+srv://Borvo:dummocoin@bivo-query-qbt1m.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

app = Flask(__name__)

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Web application to send Data Orders'
    )

@app.route('/createDataOrder', methods = ['POST'])
def createDataOrder():
    """Parses through input JSON file and outputs a JSON file to send to data order server"""
    dataIn = request.get_json()

    host_name = socket.gethostname()
    host_IP = socket.gethostbyname(host_name)

    dd = db.dataOrders.insert_one({
           "audience": dataIn.get('audience'),
           "query": dataIn.get('query'),
           "bio": dataIn.get('bio'),
           "serverAddress": 'http://127.0.0.1:3000/sendData'
          })

    orderID = dd.inserted_id

    my_dict = {}
    my_dict['audience'] = dataIn.get('audience')        #audience will be an array of audience attributes
    my_dict['query'] = dataIn.get('query')              #query will be an array of query attributes
    my_dict['bio'] = dataIn.get('bio')                  #bio will be a string describing study
    my_dict['serverAddress'] = 'http://127.0.0.1:3000/sendData'     #localhost is 127.0.0.1
    my_dict['orderID'] = orderID
    order = jsonify(my_dict)

    response = requests.post("https://127.0.0.1:80/dataOrder", req = order)
    return "Data Sent"

@app.route('/transferData', methods = ['POST'])
def transfer():
    """Transfers data to the researcher's server"""
    dataIn = request.get_json()
    my_dict['encrypted_data'] = dataIn.get('data')      #data will be a vector of data points
    my_dict['orderID'] = dataIn.get('orderID')
    dataOut = jsonify(my_dict)

    response = requests.post("https://127.0.0.1:3000/transferData", req = dataOut)

    return "Data Received"


app.run(host = "0.0.0.0", port = int('3000'), debug = True)

    
