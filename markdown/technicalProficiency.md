---
layout: default
title: 'Technical Proficiency'
permalink: technicalProficiency
---
## What is the overall quality of your code?

For the purposes of answering this question succinctly, I will use the script called mqtt_Listen_Sensor_Data.py as the best example of my overall code quality.
The script’s original author is Pradeep Singh, and I want to credit the original author. He has done a good job introducing the MQTT protocol to Python.  
The script assumes the reader already knows several things: what Mongo is and how it stores data, what LoRa is and how the network operates, what MQTT is and the basic layout of LoRa MQTT messages. I would advise anyone who wants to use this script to familiarize themselves with these concepts before using it.

The layout is fairly simple. The first section loads the static and default variables. If the user has passed in any arguments, the default variables are overwritten with the new arguments. There is no error checking to see if the argument syntax is correct.

The next section defines the two JSON objects used in the database as classes; NodeEntry and DataEntry. Anyone familiar with LoRa nodes will easily recognize the class structure.

The third section defines the MQTT methods required for connecting and subscribing to an MQTT publisher, and the method for processing MQTT messages. The processing is more involved than other parts of the script and so alongside the process is comments describing each action.

For example, one section of the script converts a string representation of a datetime and converts it to the BSON readable ISO-datetime format. This is a confusing line of code even to me, but the functionality is explained in the comments:
```
# create the json from the data_entry object
# from https://stackoverflow.com/questions/127803
# Take the string for 'time' and convert into ISO-datetime format 8601DZ
data_entry = DataEntry(message_json['data'], datetime.datetime.strptime(message_json['rxInfo'][0]['time'], "%Y-%m-%dT%H:%M:%S.%fZ"))
```
In the comments, I include the source from stackoverflow.com even though answers from StackOverflow are badly reputed. The answer I found was accurate and works for converting RFC 3339 to ISO 8601DZ.  
Other answers I found were for parsing dates of unknown format such as dateutil.parser.parse. I included my source to explain my reasoning, so other people reading the script and creating modified or improved versions would be able to keep the original date parsing or choose an alternative.

The final section runs the script. It is short and self explanatory.

Overall my code is easy to read because it is divided into easily read sections and covers all relevant use cases.

In conclusion, my style of writing code gives peers an easy understanding of the structure and logic. Some variables and class structures are not as flexible or modular as they could be, and I have a weakness when naming variables; I often give them names that do not convey their purpose clearly. I am trying to improve my variable naming with practice. But clear commenting and script structure are key parts of my code quality.

## How well did you follow best practices in development?

**Task volunteering**  
Tasks were open to volunteers at the start of the semester. Each student was allowed to select the task that appealed to them most.

**Testing**  
Unit tests are an important practice for all Agile development projects. Our project had no focus on unit tests, but we did test our products by using them in the real world, ensuring that communication worked from end to end.  
This did reveal several bugs that we weren't aware of before, such as blocked ports on the Polytechnic network. 

**Refactoring**  
Real world testing has shown us where our code needed improvement. My personal example of this is in the mqtt_Listen_Sensor_Data script, in an earlier version I uploaded every new message to the database as soon as it arrived. When it was tested, it showed that the database would quickly become bloated.  
I refactored the database structure and the script so that each node would be stored only once, and only the data and time would be added to the node data entries, significantly reducing the bloat.

## How well did you use appropriate version control?

Because our group was small and each member had their own seperate, non-conflicting project, our group fell into a centralized workflow. I regularly pushed my work to the master branch after every update, always with a message. This message was very short and often did not explain every change that was made since the last commit.  
I would like to learn how to use Git in a workplace environment, with different workflows and git commands to improve version control for future projects and to allow for smoother development alonside other developers in the group.

## To what extent do you think you contributed an equal portion of the overall project?

I feel that my contribution was significant to the overall project, and the work I put into my tasks resulted in reusable, quality software that will be used by both future students and our users. I listened to others in our meetings and contributed my ideas and open opinions as well.