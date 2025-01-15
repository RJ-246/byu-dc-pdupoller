from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
# Create your views here.
connectionString = "mongodb://root:strongPassword@127.0.0.1:27017"

mongoClient = MongoClient(connectionString)

deviceDB = mongoClient["devices"]
modbusCollection = deviceDB["modbus"]
snmpCollection = deviceDB["snmp"]

def index(request):
    device_list = modbusCollection.find({})
    context = {
        "device_list": device_list
    }
    return render(request, "index.html", context)