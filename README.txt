Jcf2167
Jessica Fan 
Assignment 1: Computer Networks

a.) the code first builds a socket and then listens. The select module decides what to do for each input. If the input is a server socket, then the program accepts incoming clients. If the input is from the server's keyboard, then the server terminates, else the program handles input from the client socket. 

The handle() method takes care of whoelse, wholasthr, broadcast, message, block, unblock and logout. 

The user is logged out after 30 minutes of inactivity
The user is blocked for a minute if 3 consecutive logins fail. 
Multiple clients can log on and chat with each other. 

b.) 
I used sublime text 2 to code this program! 

c.) run code like this:

python server.py 4119
python client.py 10.11.12.13 4119

d.) sample commands to invoke in code:

Command:
whoelse

Command:
wholasthr

Command:
broadcast Hello There!

Command:
message wikipedia HI THERE!

Command:
block wikipedia

Command:
unblock wikipedia

Command:
logout

e.) sorry....not additional functionalities :^(
