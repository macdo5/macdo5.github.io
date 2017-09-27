"""
Original Author: Pradeep Singh
Date: 20th January 2017
Version: 1.0
Python Ver: 2.7
Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
This script subscribes to a LoRa MQTT broker, such as loraserver, Loriot or TTN.
It processes the received MQTT message into a matching mongo database format and stores it.
For mongo collection format and information, refer to documentation on GitHub.
"""

import datetime
import json
import paho.mqtt.client as mqtt
#from store_Sensor_Data_to_DB import sensor_Data_Handler
from pymongo import MongoClient
# http://api.mongodb.com/python/1.10.1/api/bson/json_util.html
# Tools for using Python's json module with BSON documents
from bson import json_util

# MQTT Settings 
MQTT_Broker = "https://iot.op-bit.nz"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "application/#" # subscribe to all incoming messages that begin with application/

# MongoDB settings
# from http://api.mongodb.com/python/current/tutorial.html
client = MongoClient()
db = client.duniot_database
mqtt_collection = db.node_data


class NodeEntry:

    def __init__(self, devEUI, nodeName, applicationID, applicationName, dataEntry=[]):
        self.data = {}  # create an empty object
        self.data['applicationName'] = applicationName
        self.data['nodeName'] = nodeName
        self.data['dataEntries'] = [dataEntry.data]
        self.data['applicationID'] = applicationID
        self.data['devEUI'] = devEUI


class DataEntry:

    def __init__(self, data, time):
        self.data = {}
        self.data["data"] = data
        self.data["gwTime"] = time


# Subscribe to the specified topic
def on_connect(mqttc, mosq, obj, rc):
    mqttc.subscribe(MQTT_Topic, 0)


# When the message is received, it is processed and stored in the database.
def on_message(mosq, obj, msg):
    # This is the Master Call for saving MQTT Data into DB
    print("MQTT Data Received...")
    print("MQTT Topic: " + msg.topic)
    # create a json object from the received mqtt data
    message_json = json.loads(msg.payload)
    print("extracting data")
    # create the json from the data_entry object
    # from https://stackoverflow.com/questions/127803
    # Take the string for 'time' and convert into ISO-datetime format 8601DZ
    data_entry = DataEntry(message_json['data'], datetime.datetime.strptime(message_json['rxInfo'][0]['time'], "%Y-%m-%dT%H:%M:%S.%fZ"))
    # print the time that the gateway received the data.
    print("time:" + str(data_entry.data["gwTime"]))
    # Add the MQTT data to MongoDB
    # First, check that the device is already in the database.
    # Check the database if at least a single item exists with the matching criteria
    # A combination of applicationID, devEUI and nodeName will ensure single unique nodes per application exist.
    # query returns a Cursor object
    found = mqtt_collection.find({
        "nodeName": message_json['nodeName'],
        "applicationID": message_json['applicationID'],
        "devEUI": message_json['devEUI']
    }).limit(1)
    # get the number of items in the cursor
    # from https://stackoverflow.com/questions/26549787
    # dynamic JSON building in python (https://stackoverflow.com/questions/23110383)
    if found.count() == 0:  # no collections exist in db matching the search criteria
        print("node not found in database, creating new node...")
        # build the new node json:
        new_node = NodeEntry(
            message_json['devEUI'],
            message_json['nodeName'],
            message_json['applicationID'],
            message_json['applicationName'],
            data_entry)
        # create the json from the node_entry object
        print("inserting into duniot_database.node_data")
        new_entry_id = mqtt_collection.insert_one(new_node.data).inserted_id
        print("Success. Node ID is " + str(new_entry_id))
    else:   # at least one collection exists, therefore add the data to the existing collection

        # push the data onto the end of the dataEntries array
        print("pushing data to data entries in database")
        # from https://stackoverflow.com/questions/31077812
        mqtt_collection.update(
            {"_id": found[0].get('_id')}, {"$push": {"dataEntries": data_entry.data}}
        )
        print("node data entries updated")


def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()
print("connecting...")
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.subscribe("#")
print("subscribed")
# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
print("connected")
# Continue the network loop
mqttc.loop_forever()

