# Personal Timeline
### Week 1
First order of business was to look at Trello to keep up to date.
I selflessly gave the old server to Patrick and let him reinstall windows over all the data. Bye-bye old server.
New server had to be setup. Fortunately I was able to follow the instructions from last semester and also the tutorials from [loraserver](https://docs.loraserver.io/overview/)
IoT meetup arranged.
### Week 2
Continue working on setting up the server like last year, add organizations, users, gateways, applications and nodes to web server.
### Week 3
Installed mqtt subscriber: mosquitto. Data that comes in from gateways is in JSON format, which should be easy to parse. 
We want to store the data persistently, so I researched different solutions to storing the data. 
Mosquitto said it has a way of storing data persistently, but this is only for queuing mqtt messages temporarily, not for a complete database solution.
I've learnt how to use SQL in the past, but with encouragement from team members (who were 'converted' by Chris Franz) I decided to research NoSQL implementations as well.
The loraserver stores information about organizations, users, gateways, applications and nodes in a PostgreQL database, but the only thing it doesn't store is data.
#### Database design.
Looking at the App server, I want to see what its parameters are and how they would match our database.
I tried to create an organization that had the same name as an existing organization. I received this error:
`Error object already exists (code: 6)`
I created an organization called **test**, then deleted it and created another organization, also called **test**.
This worked fine, and I also noticed that the ID of the organization was 7. I repeated the last step, and I saw that the ID had again incremented.
I remembered during the installation of the app server that postgres was installed and a role with a database was created.

I logged into the server using ssh, and I opened postgres as the psql role.
```
sudo -u postgres psql
\l
```
there were two databases: **loraserver_as** and **loraserver_ns**
```
\c loraserver_as
\dt
```
There were 9 tables: **application**, **application_user**, **downlink_queue**, **gateway**, **gorp_migrations**, **node**, **organization**, **organization_user**, and **user**
`SELECT * FROM organization`
This showed pretty much the same things that were displayed on the app server, with a **created_at** and **updated_at** fields.
`SELECT * FROM node`
This showed information about the node, but no information about persistent data.
I was about to design a 'node data' table, when I noticed a section in the app server for the nodes labelled **Frame logs**.
It contained a variable called 'bytes' but it wasn't the sensory data that was sent from the node. Back to designing the table.

Some group members have suggested NoSQL. Let's have a look:
##SQL vs NoSQL: which database is best suited for our data?
NoSQL:
- Used with massive volumes of new, rapidly changing data types.
- Agile development projects
- Scalable and flexible databases
- Document based, key-value pairs, graph databases or wide-column stores. No standard schema definitions which it needs to adhere to.
-- This gives it a dynamic schema for unstructured data.
### Week 4
There are several examples of people who have used MongoDB to store incoming MQTT packets. JavaScript and Python have methods for running MQTT subscribers and methods for operating MongoDB, so either language could be used to store data.
My favourite freely available script was by [Pradeep Singh](https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/), and with a bit of configuration I could run the script on our local server and store the data in a mongo database.
[See the full customized script here](https://github.com/macdo5/ThingsNetworkDunedin/blob/gh-pages/mqtt_subscribers/mqtt_Listen_Sensor_Data.py).

The main part of the script is what it does when a new message arrives:
```
def on_message(mosq, obj, msg):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    print("MQTT Data Received...")
    print("MQTT Topic: " + msg.topic)
    print(msg.payload)
    new_mqtt_data = json.loads(msg.payload)
    print("time:")
    print(new_mqtt_data['rxInfo'][0]['time'])
    # from https://stackoverflow.com/questions/127803
    # Take the string for 'time' and convert into ISO-datetime format 8601DZ
    new_mqtt_data['rxInfo'][0]['time'] = datetime.datetime.strptime(new_mqtt_data['rxInfo'][0]['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # Add the MQTT data to MongoDB
    print("inserting into duniot_database.mqtt_collection")
    new_entry_id = mqtt_collection.insert_one(new_mqtt_data).inserted_id
    print("Success. Entry ID is " + str(new_entry_id))
```
This week, we can't decode the data for some reason.
### Week 5
After leaving the script running for the weekend collecting the node information from the room sensor (about every 3 minutes), there were over 4,000 entries in the database. The database size was already 1MB large. If we store the data from hundreds of nodes over months, our database will quickly expand beyond reasonable limits!
5554 entries in the database is 2.731 MB!
The MQTT JSON contains a lot of redundant or useless info, all we want is the payload data, timestamp, and node of origin. A new database has to be designed. The node info is already in the PostgreSQL database, but that would mean combining PostgreSQL and MongoDB queries, which might not end well.

### Week 6
After dropping the database and re-writing the script, the database now collects only the relevant data.
`on-message` is now quite different:
```
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
```
The size of the database is much smaller now, but we've decided to not collect the data on the web-app server side. It's not a problem though, because we will be able to run a local server in the polytech to collect the data instead.  
We will be deploying pretty soon.

### Week 7
We're getting ready to migrate the development server onto the production server, so we needed a clean install to reduce diskspace and resource consumption on the cloud.
I did a fresh install of the ubuntu server and loraserver and it's ready to be copied and uploaded. We won't be able to store data in a mongoDB on the cloud, but we could use our own server on-site that subscribes to the cloud server and runs a mongoDB, which could be useful for future applications.
Migrated my branch folders from TheThingsNetworkDunedin to DunedinIoT on GitHub.

### Week 8
All of us are waiting for the server to go online, in the meantime we can focus on more documentation, personal timelines, our portfolios, basically any work that currently has a lower priority.

### Week 9
The LoRa server was officially deployed. The web address is https://iot.op-bit.nz:8080. We need to find a way to change the address to https://iot.op-bit.nz, to make it simpler for the user.
In the lora-app-server config file there is an option to change the web address and port number. Changing to port 80 and running the server resulted in a permissions error, even as sudo (how is that possible?)
After a bit of googling, you can use `authbind` to allow the service to run on the specified port:
```
sudo apt-get install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown dunedinadmin /etc/authbind/byport/80
sudo systemctl start lora-app-server
```
### Week 10
Website is down, and I have no idea how to fix it. Can access the website through putty but can't ping it. Talked to Michael from the BIT Platform group about it, he wasn't sure either so we took it to Rob.  
Rob said to check the firewalls for both the server and AWS itself. After opening port 80 we managed to connect to the web page again.  
Changed the default port from 80 to 443, now webpage url loads without specifying a port number  
Installing CA certificates, from `https://letsencrypt.org/getting-started/`:  
`We recommend that most people with shell access use the Certbot ACME client.`  
from `https://certbot.eff.org/#ubuntuxenial-other`:  
```
$ sudo apt-get update
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot 
```
`If you already have a webserver running, we recommend choosing the "webroot" plugin. To obtain a cert using the "webroot" plugin, which can work with the webroot directory of any webserver software:`  
from `https://www.digitalocean.com/community/tutorials/how-to-use-certbot-standalone-mode-to-retrieve-let-s-encrypt-ssl-certificates`  
`dunedinadmin@ubuntu:/etc/lora-app-server/certs$ sudo certbot certonly --standalone --preferred-challenges tls-sni -d iot.op-bit.nz`
Edit the HTTP_TLS_CERT variable to /etc/letsencrypt/live/iot.op-bit.nz/fullchain.pem and HTTP_TLS_KEY to /etc/letsencrypt/live/iot.op-bit.nz/privkey.pem
`crontab -e`
`0 02 01 */3 * certbot renew`
Will run every three months at 03:30 on the 1st of Jan,Apr,Jul and Oct.  
  
After hitting a problem wile running the lora-app-process (permission denied on a .pem file), I tried adding a new group that the user appserver would be part of, and would give permission to access the file.

### Week 11
Nothing new to report

### Week 12
To prepare for the showcase, I will recreate the Mongo database on our local server. We can use it to show graphs representing node data over time.
Our showcase will display water moisture of a potplant from 2-3 kms away (almost a 'hello world' for IoT projects). I will collect data of water moisture
over time from a single pot plant. I have a few at home that I could use. Failing that, we can fabricate some data, as long as we can display a graph for showcase.
A new web app for the showcase has started, and it will require using an MQTT subscription. My mqtt_Listen_Sensor_Data script can be converted into
JavaScript, or Thomas' script can be used to subscribe to the moisture MQTT application.

### Week 13
I tried running Thomas' JavaScript for subscribing to our server but it had an error: `WebSocket connection to 'ws://iot.op-bit.nz:1884/mqtt' failed: Error in connection establishment: net::ERR_CONNECTION_TIMED_OUT`. I'll get back to that later.
### Week 14
Thomas' JavaScript relies on a websocket and the server is currently only listening on the mqtt port 1883. 
We have to create another listener on port 1884 using the websocket protocol. That can be done by editing the mosquitto.conf file, much like in this article:
`https://tech.scargill.net/mosquitto-and-web-sockets/`.  
We won't be able to test it on the Polytechnic network because that requires asking the network admin to open port 1884 for us. He's opened ports one by one 
for about 5 ports now and he's getting sick of it. I assured him we would only bother him with a list of ports by 06/11/17 or not at all. He suggested we 
use a single device and a network rule to allow all communication through all ports between that device and our server, but that wouldn't work for us 
because our users will be using different devices. It shouldn't matter at this point, with any luck there will be no more ports to open.  
While we wait for that port to open, we can still use the mqtt protocol for non-browsers, and we can test our code using `test.mosquitto.org` or similar. 
I have the Mongo database back up and running, we just need to start gathering data for it and make sure that devices on the OP-Guest network can connect to
it.
