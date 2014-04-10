import select 
import socket 
import sys 
import time

global block_time_start
block_time_start={}

#in minutes
global TIME_OUT
TIME_OUT=30

#in minutes
global LAST_HOUR
LAST_HOUR=60

global active
active=[]

global lastActive
lastActive={}

global blockedUsersOf
blockedUsersOf={}

global addressOf
addressOf={}

#in seconds
global BLOCK_TIME
BLOCK_TIME=60

global input
input=[]

global lines
lines=[]

global userTime
userTime={} 

global offlineMessages
offlineMessages={}

global isAlive
isAlive={}

def doWhoelse():
    count=0
    for i in input:
        if type(server)==type(i):
            count+=1 #add each socket object to count 
    count-=1 #don't include server socket 
    for x in active:
            s.send(x)
	    s.send("\n")
    s.send("There are: " + str(count) + " people online. \n")

def handle(c, IP): #c is userinputted command (ie: message facebook butts)
    username=""
    for key in addressOf:
        if addressOf[key]==IP:
            username=key
    strarray=c.split(" ") 
    command=strarray[0] 
    print command #####################################
    #command options are: whoelse, wholasthr, broadcast, message, block, unblock, logout
    lastActive[IP]=time.time()
    if command=="whoelse":
        doWhoelse()
        command="" #reset command 
        s.send("Command: ")  #resent command request 
        return #return to while loop in main 

    elif command == "wholasthr": 
        lasthour=time.time()-(LAST_HOUR*60) #gets range of last hour 
        tempd={} #temporary dict for mutating userTime 

        for key in userTime:
            if userTime[key]>=lasthour:
                tempd[key]=userTime[key] #only has last hour users in new dict

        userTime.clear() #clear old dict

        for k in tempd:
            userTime[k]=tempd[k] #copy new dict into old dict

        s.send("These were the users online in the last hour: ")
        for key in userTime:
           s.send(key)#for each entry in old dict, send to client 
           s.send("\n") 

        command="" #reset command etc. 
        s.send("Command: ")
        return
    elif command=="getIP":
        s.send("This is your IP " + IP)

    elif command=="broadcast": 
        msg=username+" has broadcasted publically " + " \"" +c.replace("broadcast", "").strip() +"\""
        for i in input: #for each input 
            if type(i)==type(server) and i!=server:#if socketobject and is not server 
                i.send(msg) #send the message 
        command="" 
        s.send("Command: ")
        return

    elif command=="message":
        online=False #boolean to see if need to store message 
        str=c.replace("message","").strip()  
        arr=str.split(' ', 1)              #parse message
        sender=username                 #get sender
        reciever=arr[0]                     #get reciever 
        message=arr[1]                  #get msg

        #if reciever specified blocked list
        #and if sender is on recievers blocked list
        if reciever in blockedUsersOf and sender in blockedUsersOf[reciever]: #if sender is blocked
                s.send(reciever + " has blocked you. You cannot send them any messages")
		s.send("\n")
        else:
            #for each input 
            for i in input:
                #trying to find right user 
                #if socket and is not server and same updated IP as username 
                if type(i)==type(server) and i!=server and reciever in addressOf and i.getpeername()[0]==addressOf[reciever]: 
                    #then user is online--> sends message
                    online=True
                    str=message + "--from " + sender + "\n"
                    i.send(str)
            #if offline, store in offline DB
            if online==False: 
                s.send("Sorry this user is not on right now but we will send the message when they log on!")
                offlineMessages[reciever]= message + " --from " + sender
        sender=""
        reciever=""
        message = ""
        command=""
        s.send("Command: ")
        return
    
    elif command == "block":
        user=c.replace("block", "").strip() 
        if user==username: #error message for if you try and block yourself 
            s.send("you cant block yourself!!")
        else: 
            s.send(user + " will be blocked.")
            if username not in blockedUsersOf: #if there isnt dict entry for blockedUsersOf
                blockedUsersOf[username]=[] #MAKE ONe
                blockedUsersOf[username].append(user)
            else:
                blockedUsersOf[username].append(user)
            s.send("This is your blocked list of users:")
            for i in blockedUsersOf[username]:
                s.send(i + " ") 
        s.send("\n")
        command=""
        s.send("Command: ")
        return

    elif command == "unblock":
        user=c.replace("unblock", "").strip()

        if user in blockedUsersOf[username]:
            s.send(user + " will be unblocked.")
            blockedUsersOf[username].remove(user)

        else:
            s.send("This user is not on your blocked list to begin with.\n")

        s.send("This is your blocked list of users:")

        for i in blockedUsersOf[username]:
            s.send(i)
        s.send("\n")
        command=""
        s.send("Command: ")
        return
    
    elif command == "logout":
        s.close()
        input.remove(s)
        active.remove(username)

    else: 
        s.send("Invalid command, please type again...")
        command=""
        s.send("Command: ")
        return

    

def authenticate():
    dontAsk=False
    b=False
    client.send("Username: ")
    username=client.recv(size)
    username=username.strip()
    if username in active: 
        client.send("Sorry! Looks like this user is already logged on!")
        return dontAsk, b,username
    if username in block_time_start:
        if (round(time.time())-block_time_start[username]) < BLOCK_TIME:
            client.send("You have been blocked for " + str(round(time.time())-block_time_start[username]) + " seconds." )
            dontAsk=True
        else:
            client.send("Okay," + str(BLOCK_TIME)+ " seconds is up. You're unblocked now. Try Again.")
            del block_time_start[username]
            dontAsk=False
    client.send("Password: ")
    pw=client.recv(size)
    pw=pw.strip()
    for line in lines:
        part=line.split(" ")
        if username==part[0] and pw==part[1]:
            b=True
             
    return dontAsk, b,username

def login(client):

    dontAsk, isUser, username=authenticate()
    count = 0
    while isUser==False and count <3:
        dontAsk, isUser, username=authenticate()
        if isUser==True:
            break
        elif dontAsk:
            count=0 
        else:
            client.send("Error: wrong password. Try Again")
            count+=1

    if isUser==False and count==3:
        client.send("You're being blocked for " + str(BLOCK_TIME)+ " seconds! ")
        block_time_start[username]=round(time.time())
        return "bad" 

    if isUser==True:
        return username

def seeOfflineMessages(username):
    for key in offlineMessages: #for each username  in offlineMessages dict
        client.send("These were your offline messages!")
        client.send("\n")
        if key == username: #if this user's dict entry
             client.send(offlineMessages[key]) #send user all offline messages 
             offlineMessages[key]=[] #empty out dict entry
    client.send("\n")

def checkActive():
    for i in input:
        if type(i)==type(server) and i!=server:
            if i.getpeername()[0] in lastActive:
                range=lasthour=time.time()-(TIME_OUT*60)
                if lastActive[i.getpeername()[0]]<=range:
                    s.close()
                    input.remove(s)
                    active.remove(username)

#sets up the server 
host = '' 
port = int(sys.argv[1]) 
size = 1024 
lines= [line.strip() for line in open('user_pass.txt')]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(1) 
input = [server,sys.stdin] 
run= 1 
print "Starting"
while run: 
    checkActive()
    inputready,outputready,exceptready = select.select(input,[],[]) 
    for s in inputready: 
        if s == server:
            # handle the server socket 
            client, address = server.accept() 
            username=login(client)  #verifies input username 
            if username=="bad":
                client.close()
            else:
                active.append(username)
                input.append(client) #puts client socket into input 
                addressOf[username]=client.getpeername()[0]   #updates dictionary of username's lastest IP
                userTime[username]=time.time() #updates dict of time when user logged in
                lastActive[address[0]]=time.time()
                client.send("Welcome to simple chat server!") #warm welome ._.
                seeOfflineMessages(username)  #shows offline messages
                client.send("Command: ") #ask for first command:
        elif s == sys.stdin: 
            # handle standard input 
            junk = sys.stdin.readline() 
            running = 0  #shuts down server, dont touch server keyboard

        else:
            # handle incoming messages from client s 
            command = s.recv(size).strip() #gets user entry command w/o trailing \n
            handle(command, s.getpeername()[0]) #handle that shit bro. 
            break

server.close()

