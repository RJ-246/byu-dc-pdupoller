from flask import Flask
from pymongo import MongoClient
# Create your views here.


app = Flask(__name__)
connectionString = "mongodb://root:strongPassword@127.0.0.1:27017"

mongoClient = MongoClient(connectionString)

deviceDB = mongoClient["devices"]
modbusCollection = deviceDB["modbus"]
snmpCollection = deviceDB["snmp"]

@app.route("/")
def index():

    return "<p>Hello world </p>"

@app.route("/devices")
def devices():
    device_list = modbusCollection.find({})
    context = {
       "device_list": device_list
    }

@app.post("/devices/add")
def add_device():
    return