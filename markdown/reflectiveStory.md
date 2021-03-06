---
layout: default
title: 'Reflective Story'
permalink: reflectiveStory
---

# Reflective Story
## Reconstructing the server
A lot of the work I did in the first few weeks of the second semester was the same as the work I had done in the first. It might seem stupid to do the same things twice but it gave me the opportunity to reinforce what I learnt and gave me a lot more confidence in my abilities. I created a step-by-step tutorial for deploying the loraserver on an Ubuntu machine which can be viewed [on our github repo](https://github.com/OtagoPolytechnic/DunedinIoT/tree/gh-pages/development/servers).
I know that the project experience here in Otago Polytech is a lot different to the intensity of the workplace, with looming deadlines and crushing responsibility, but the way we handled our project development and spending time to create proper documentation has resulted in an impressive product for just a bunch of students.

## Working with JSON
One of my favourite things I've learnt this semester is that people (or most of them) really like JSON or JSON-ish data. It's really easy to parse, even between languages. It's great for storing timestamps, geolocations, collections, and it's human readable. I'm really glad I've got nothing to do with XML, I've tried parsing it in Java and it gave me a headache.  

## Self education: Learning MongoDB
I've also learnt how to use MongoDB on my own this semester. I made my own research and [documented](markdown/MongoDB research and testing.md) my findings and unserstanding. NoSQL and Mongo in particular are not well reputed (at least from some people I've talked to). An example entry of our Mongo database can be found [here](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/mongo/revised%20mongo%20collection.json) Even if Mongo turns out to be a complete flop at least I've learnt a bit more about how to learn about something. There should be an entire field of IT for self-applied research. They don't teach you how to learn things on your own, and by learning how to use MongoDB on my own I've learnt a bit more about how to teach myself new skills. If I want to get a job and keep it (or at least still qualify for new jobs), I'll have to continue expanding my IT skills but also how to teach myself.  

## Self education: Installing CA certificates
I also had to learn how to install CA certificates by myself, which is as simple as following the instructions on the CA certifiers website. [Link to the documentation of certificate configuration](markdown/ca_certificate_setup.md). It's a great feeling to see your server deployed on an official website using https, it makes it feel authentic.
Otago Polytechnic does include a bit of self-motivated teaching, one of the practicals involves learning how to use a new language and another is about a new tool for programming (APIs or something similar). But two practicals don't really cover everything, you need to practice a lot more than that!  

## Self education: Evaluation
Part of the self-education includes deciding for yourself which equivalent tool are you going to use for the next project. In my case it was the decision between SQL and NoSQL. NoSQL won for two reasons: 
1. It's a new field that I would have to teach myself, improving my skills.
2. It stores objects using JSON-ish syntax, which works well with the JSON that the gateway sends to the server.  
Learning about new Python tools like [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.1 "About MQTT Python client library") and creating graphs using [matplotlib](https://matplotlib.org/) was really fun and informative, definitely skills I will be able to use in the future. The [show_data.py](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/mongo/show_data.py) is my script to create a graph of humidity and temperature changes over time.

## Refactoring for efficiency
Perhaps I wouldn't have had the bloated database problem if I had used SQL, but even so I managed to create a solution that removed the bloating. In the end I think SQL and NoSQL have their advantages and disadvantages, depending on what their use is.  
It's also been really fun to create my own web portfolio. It will be useful while looking for employment, and I will be able to continue developing code and displaying it on my portfolio.

## Brushing up on JavaScript
The loraserver has an API that can authenticate users and provide useful queries and commands, so I created a basic [JavaScript request script](https://github.com/macdo5/macdo5.github.io/blob/master/DunedinIoT_code/js%20API%20calls/loraserverAPIcall.js) to demonstrate what it could do. This script accepts a username and password, and prints all nodes from application 3. It makes two http requests: the first uses the username and password which returns a JSON Web Token (JWT) as temporary authentication. The second request uses the JWT to query the server for all nodes from application 3 and prints the result before finishing. This was just an example script to show what the app server could do, and there are many more uses for the API. All requests can be found at https://iot.op-bit.nz/api. It was several months since I used JavaScript so I had to brush up on my XmlHttpRequests skills while writing the script. 