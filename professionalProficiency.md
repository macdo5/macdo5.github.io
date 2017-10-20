Project 2 - Professional Proficiency

1. How often do you attend scheduled group meetings/scrums?

I attend every scheduled group meeting and scrum. I take notes in every meeting and I have the meeting notes for each one.

2. How well did you communicate with others in your group or subgroup?

I received slack notifications on my phone and computer so I was always in touch. The open office space was also useful as it allowed us to communicate in the office with ease.  

3. How well did you document your work throughout the project?

When creating the initial server, each step was documented. Using th documentation, we were able to create a simplified step-by-step tutorial to recreate the server.  
Code documentation was included in the comments.

4. How well did you respond to problems or changing requirements?

One of the main problems I had to fix was the blocked port issue; accessing the web server was not possible on the default port 8080 and MQTT messages couldn't be sent or received on port 1883.  
We were able to fix the web server port issue by changing the port to 443, which is already open on the polytechnic firewall. To allow MQTT through the Polytechnic firewall we had to ask our systems administrator Rob to go through the process of opening port 1883.  
While we were waiting for the port to open, we were able to temporarily work around the issue by using a different network; we were able to subscribe to our MQTT web server from home or by using cellular data.