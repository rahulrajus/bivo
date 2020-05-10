"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template
from BiVOsendRequest import app
from pymongo import MongoClient
import json
import requests
from flask_socketio import SocketIO, send, emit

client = MongoClient("mongodb+srv://Borvo:dummocoin@bivo-query-qbt1m.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

app = Flask(__name__)
sio = SocketIO(app)


def sendJSON(json):
    print('received data: ' + str(json))
    send(json, namespace = '/sending')

@sio.on('disconnect')
def disconnect():
    print('Client Disconnected')

@sio.on('connect')
def connection():
    print('Client Connected')

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

    dd = db.dataOrders.insert_one({
           "audience": dataIn.get('audience'),
           "query": dataIn.get('query'),
           "university": dataIn.get('university'),
           "research_type": dataIn.get('research_type'),
           "price": dataIn.get('price'),
           "bio": dataIn.get('bio'),
           "serverAddress": 'http://f7e896cf.ngrok.io/transferData'
          })

    orderID = dd.inserted_id

    my_dict = {}
    my_dict['audience'] = dataIn.get('audience')        #audience will be an array of audience attributes
    my_dict['query'] = dataIn.get('query').get('data')              #query will be an array of query attributes
    my_dict['university'] = dataIn.get('university')
    my_dict['research_type'] = dataIn.get('research_type')
    my_dict['price'] = dataIn.get('price')
    my_dict['bio'] = dataIn.get('bio')                 #bio will be a string describing study
    my_dict['serverAddress'] = 'http://f7e896cf.ngrok.io/transferData'     #localhost is 127.0.0.1
    my_dict['orderId'] = str(orderID)
    #order = jsonify(my_dict)
    print(my_dict)
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://ee1cab2e.ngrok.io/dataOrder", json = my_dict, headers = headers)
    return "Data Sent"

@app.route('/transferData', methods = ['POST'])
def transferData():
    """Transfers data to the researcher's server"""
    dataIn = request.get_json()
    print(dataIn)
    my_dict = {}
    my_dict['encrypted_data'] = dataIn.get('data')      #data will be an array of headers pointing to arrays of data points
    my_dict['orderId'] = dataIn.get('orderId')
    dataOut = jsonify(my_dict)

    datum = db.dataValues.insert_one({
           "data": dataIn.get('data'),
           "orderId": dataIn.get('orderId'),
          })

    sendJSON(dataOut)
    return "Data Received"

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = int('3000'), debug = True)
    sio.run(app, host = "0.0.0.0", port = int('4000'))
    
