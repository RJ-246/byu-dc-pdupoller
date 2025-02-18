from bson import json_util, ObjectId
from pymongo import MongoClient
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import logging
## prometheus setup



#logging
logging.basicConfig(filename="output.log",
                    format='%(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)



bp = Blueprint('devices', __name__, static_folder='static', url_prefix="/devices")



# Database connection
connectionString = "mongodb://root:strongPassword@mongodb:27017"

mongoClient = MongoClient(connectionString)

deviceDB = mongoClient["devices"]
modbusCollection = deviceDB["modbus"]
snmpCollection = deviceDB["snmp"]


@bp.route('get_all_modbus')
def get_all_modbus():
    device_cursor = modbusCollection.find({})
    device_list = []
    for device in device_cursor:
        device_list.append(device)
    return json_util.dumps(device_list)

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
    return render_template('devices/deviceTable.html', context=context)

@bp.get('/add')
def addDevice_get():
    return render_template('devices/addDevice.html')

@bp.post('/add')
def addDevice_post():
    # Get list of registers from form
    registers = request.form.getlist("register[][register]")
    read_counts = request.form.getlist("register[][read_count]")
    slaves = request.form.getlist("register[][slave]")
    metric_names = request.form.getlist("register[][metric_name]")
    metric_units = request.form.getlist("register[][metric_unit]")
    groupings = request.form.getlist("register[][grouping]")

    register_list = [
        {
         'register': register,
         "read_count": read_count,
         "slave": slave,
         "metric_name": metric_name,
         "metric_unit": metric_unit,
         "grouping": grouping
         }
        for register, read_count, slave, metric_name, metric_unit, grouping in zip(registers,read_counts, slaves, metric_names, metric_units, groupings)
        
    ]
    # Create record for insertion to mongoDB
    record = {
    "device_name": request.form['device_name'],
    "device_ip": request.form['device_ip'],
    "device_port": request.form['device_port'],
    "device_poll_type": request.form['poll_type'],
    "device_power_limit": request.form['power_limit'],
    "device_registers": register_list
    }
    record_id = ""
    
    # Insert Record
    if record["device_poll_type"] == "snmp":
        record_id = snmpCollection.insert_one(record)
    elif record["device_poll_type"] == "modbus":
        record_id = modbusCollection.insert_one(record)
    print(record_id)
    
    return redirect(url_for('devices.deviceTable'))


@bp.get('/editDevice/<device_type>/<device_id>')
def editDevice_get(device_type, device_id):
    device_id = ObjectId(device_id)
    if device_type == "modbus":
        device = modbusCollection.find_one({"_id": device_id})
    elif device_type == "snmp":
        device = snmpCollection.find_one({"_id": device_id})
    else:
        return redirect(url_for('devices.deviceTable'))
    return render_template('devices/editDevice.html', context=device)

@bp.post('/editDevice')
def editDevice_post():

    registers = request.form.getlist("register[][register]")
    read_counts = request.form.getlist("register[][read_count]")
    slaves = request.form.getlist("register[][slave]")
    metric_names = request.form.getlist("register[][metric_name]")
    metric_units = request.form.getlist("register[][metric_unit]")
    groupings = request.form.getlist("register[][grouping]")

    register_list = [
        {
         'register': register,
         "read_count": read_count,
         "slave": slave,
         "metric_name": metric_name,
         "metric_unit": metric_unit,
         "grouping": grouping
         }
        for register, read_count, slave, metric_name, metric_unit, grouping in zip(registers,read_counts, slaves, metric_names, metric_units, groupings)
        
    ]
    # Create record for insertion to mongoDB
    record = {
    "device_name": request.form['device_name'],
    "device_ip": request.form['device_ip'],
    "device_port": request.form['device_port'],
    "device_poll_type": request.form['poll_type'],
    "device_power_limit": request.form['power_limit'],
    "device_registers": register_list
    }
    record_id = request.form['device_id']

    if record['device_poll_type'] == "modbus":
        modbusCollection.update_one({"_id": ObjectId(record_id)}, {"$set": record})
    elif record['device_poll_type'] == "snmp":
        snmpCollection.update_one({"_id": ObjectId(record_id)}, {"$set": record})
    return redirect(url_for('devices.deviceTable'))