---
layout: default
title: 'Semester 2 Tasks'
permalink: semester2Tasks
---

# Semester 2 Tasks
## Task 1: Deploy loraserver to Amazon Web Services
Deploy [loraserver](https://www.loraserver.io/) to AWS. App Server can be found on [iot.op-bit.nz](https://iot.op-bit.nz).  
Configure port access with local network administrator.  
Arrange certificate authority with let's encrypt. [Documentation of process](markdown/ca_certificate_setup.md).  

## Task 2: Persistent data storage using MongoDB
Research MongoDB. [Record of research process](markdown/MongoDB research and testing.md)
Create Mongo collection structure. [Example of collection entry](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/mongo/revised%20mongo%20collection.json).  
Create Python script to subscribe to MQTT and load packages into Mongo. [Python script](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/mqtt_subscribers/mqtt_Listen_Sensor_Data.py).  
Visually represent data from Mongo collection. [Python script](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/mongo/show_data.py).

## Task 3: Verification with loraserver API using JavaScript
Research (LoRa App Server API)[https://docs.loraserver.io/lora-app-server/integrate/api/] and create API verification and query sample [script](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/js%20API%20calls/loraserverAPIcall.js).


## Task 4: Field testing
Travel with the mDot node and monitor packages to see what range the mDot can send data to the gateway.