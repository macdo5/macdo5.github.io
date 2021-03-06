---
layout: default
title: 'Professional Proficiency'
permalink: professionalProficiency
---
# Project 2 - Professional Proficiency

## How often do you attend scheduled group meetings/scrums?

I attend every scheduled group meeting and scrum. I take notes in every meeting.

## How well did you communicate with others in your group or subgroup?

I received slack notifications on my phone and computer so I was always in touch. The open office space was also useful as it allowed us to communicate in the office with ease.
I wanted to be approachable and friendly to my peers, so I was always happy to answer questions at any time.

## How well did you document your work throughout the project?

When creating the initial server, each step was documented. Using the documentation, we were able to create a simplified [step-by-step tutorial](https://github.com/OtagoPolytechnic/DunedinIoT/tree/gh-pages/development/servers) to recreate the server.  
Code documentation was included in the comments, with header comments explaining the purpose of the script and inline comments.

## How well did you respond to problems or changing requirements?

One of the main problems I had to fix was the blocked port issue; when we moved the dev to prod, accessing the web server was not possible on the default port and MQTT messages couldn't be sent or received on the MQTT port. We had just assumed everything would work on the prod because there had been no issues on the dev.
We were able to fix the web server port issue by changing the port to one that was already open on the polytechnic firewall. To allow MQTT through the Polytechnic firewall we had to ask our systems administrator Rob to go through the process of opening the port.  
While we were waiting for the port to open, we were able to temporarily work around the issue by using a different network; we were able to subscribe to our MQTT web server from home or by using cellular data.  
Another problem I discovered was that the MongoDB was becoming bloated. I had to refactor the script so that there was no data duplication in the server.
The step to solving these problems were
- identifying the source of the issue.
- considering the possible solutions and choosing the solution with the best outcome.
- taking the steps neccessary to apply the solution. 