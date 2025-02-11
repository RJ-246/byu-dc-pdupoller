import json
from pymongo import MongoClient
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('devices', __name__, static_folder='static', url_prefix="/devices")



# Database connection
connectionString = "mongodb://root:strongPassword@127.0.0.1:27017"

mongoClient = MongoClient(connectionString)

deviceDB = mongoClient["devices"]
modbusCollection = deviceDB["modbus"]
snmpCollection = deviceDB["snmp"]


@bp.route('')
def deviceTable():
    device_cursor = modbusCollection.find({})
    device_list = []
    for device in device_cursor:
        device_list.append(device)
    context = {
    # "device_list": json.dumps(device_list, default=str)
    'device_list': device_list
    }
    print(context)
    return render_template('devices/deviceTable.html', context=context)

@bp.route('/add')
def addDevice():
    return render_template('devices/addDevice.html')