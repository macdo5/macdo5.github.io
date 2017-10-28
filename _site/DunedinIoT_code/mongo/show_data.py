import datetime
import json
from pymongo import MongoClient
from bson import json_util
import numpy as np
import matplotlib.pyplot as plt
import base64
import Tkinter
# This script connects to a local Mongo Database and extracts the data from a particular node in the database
# A graph is then created using pyplot showing the data change over time
# In this example, the data contains light, humidity and temperature. The temperature is extracted and used in the graph 
# example from https://plot.ly/python/line-charts/

client = MongoClient()		# connect to the local Mongo client
db = client.duniot_database	# connect to the duniot_database
node_data = db.node_data	# connect to the node_data collection

devEUI = "0000000000000001"	# the ID for the device (node) that we want to collect the data from.

# get the dataEntries BSON object from the database by searching for the devEUI and convert into JSON
# for some reason, the BSON must be serialized and then deserialized before it can be collected
my_node_data = json_util.loads(json_util.dumps(node_data.find({"devEUI" : devEUI})))[0]["dataEntries"]

# create an array of dates and data to use in the graph.
# each date has a corresponding datum.
dates = []
data = []
for entry in my_node:
    dates.append(entry["gwTime"]) # add the date to the dates array
    y = base64.b64decode(entry["data"]).split()[2] # extract the datum (temperature)
    data.append(float(y[2:]))	# add the datum to the data array

# create the graph
plt.xlabel('time')
plt.ylabel('temperature')
plt.plot(dates, data)
plt.show()