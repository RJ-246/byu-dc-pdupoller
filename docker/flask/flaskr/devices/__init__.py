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

@bp.get('/add')
def addDevice_get():
    return render_template('devices/addDevice.html')

@bp.post('/add')
def addDevice_post():
    record = {
    "device_name": request.form['device_name'],
    "device_ip": request.form['device_ip'],
    "device_port": request.form['device_port'],
    "device_poll_type": request.form['poll_type'],
    "device_registers": []
    }
    record_id = ""
    
    if record["device_poll_type"] == "snmp":
        record_id = snmpCollection.insert_one(record)
    elif record["device_poll_type"] == "modbus":
        record_id = modbusCollection.insert_one(record)
    print(record_id)
    
    return redirect(url_for('devices.deviceTable'))