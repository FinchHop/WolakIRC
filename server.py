
# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from threading import *
from channel_list import *
from random import randint
  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

Port = 6667


# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
#IP_address = "127.0.0.1"

  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 

list_of_clients = []
list_of_channels = channel_list()
list_of_commands = ["/list - Lists all Commands",
                    "/create [name] - Create new channel called [name]\n",
                    "/remove [name] - Delete a channel called [name]\n"
                    "/join [name] - Join a channel called [name]\n"
                    "/leave [name] - Leave channel called [name]\n",
                    "/members [name] - List members of channel [name]\n",
                    "/exit - Leave the chat client\n",
                    "/id - Find out your Username\n"]
  
def clientthread(conn, addr, nickname): 
  
    # sends a message to the client whose user object is conn 
    conn.send("Welcome to this chatroom! Enter in '/commands' for a list of all commands.")
    conn.send("\nTo send a message to a channel, start with a channel name seperate by '>' followed by a message.")
    conn.send("\nFor example, 'General> Hello there!' ")
    conn.send("\nYour nickname is: " + nickname)
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message and message[0] == '/': #We deal with a specific message to a server
                    message_to_server(message, conn, nickname) #Seperate function for if section
                    

                elif message: 
 
                    chans = message.split('>',1) #Ensures we only split on the first ">"

                    if list_of_channels.check_valid_channel(chans[0]) == False: #Check if valid
                        private_broadcast("CHANNEL NAME NOT INCLUDED OR NOT VALID", conn)
                    elif list_of_channels.check_user_in_channel(chans[0], nickname) == False:
                        private_broadcast("USER NOT IN CHANNEL-MUST JOIN FIRST", conn)
                    else:
                        conns_list = list_of_channels.return_conns_in_channel(chans[0])
                        msg = "[" + chans[0] + "] " + "<" + nickname + "> " + chans[1]
                        channel_broadcast(msg, conns_list, conn)
                        print (msg)
  
            except: #Just keep swimming with exception
                continue

    return


def message_to_server(message, conn, nickname): #Giant nested if section-all cases are handled in the server, don't want user to deal
    command = message.split()
    print(command[0])
    if command[0] == "/list":
        to_send = list_of_channels.display_all()
        print(to_send)
        private_broadcast(to_send, conn)
    if command[0] == "/members":
        check = check_valid_len_and_channel(command)
        if check == False:
            return
        else:
            msg = list_of_channels.return_users_in_channel(command[1])
            private_broadcast(msg, conn)
    if command[0] == "/join":
        check = check_valid_len_and_channel(command)
        if check == False:
            return
        else:
            list_of_channels.add_user_to_channel(command[1], nickname, conn)
    if command[0] == "/leave":
        check = check_valid_len_and_channel(command)
        check_user = list_of_channels.check_user_in_channel(command[1],nickname)
        if check == False or check_user == False:
            return
        else:
            print(command[1])
            catch = list_of_channels.remove_user_single_channel(command[1], nickname)
            print(catch)
    if command[0] == "/create":
        if len(command) == 1:
            msg = "Must include new channel name after command"
            private_broadcast(msg, conn)
        elif command[1][0] == '/': #Prevents issues with trying to message channel(s) vs trying to message server
            msg = "Name of channel cannot start with '/' "
            private_broadcast(msg, conn)
        elif command[1][-1] == '>':
            msg = "End of channel cannot end with '>'"
            private_broadcast(msg,conn)
        else:
            print("Adding " + command[1])
            list_of_channels.add_channel(command[1])
            list_of_channels.add_user_to_channel(command[1], nickname, conn)
    if command[0] == "/remove":
        check = check_valid_len_and_channel(command)
        if check == False:
            return
        if command[1] == "General":
            msg = "Cannot delete General"
            private_broadcast(msg, conn)
        else:
            list_of_channels.remove(command[1])
    if command[0] == "/commands":
        for x in list_of_commands:
            print(x)
            private_broadcast(x, conn)
    if command[0] == "/exit": #exit is complex-this is server side exit
        list_of_channels.remove_user_all_channels(nickname) #removes user from all channels
        message_to_send = "<" + nickname + "> Has Exited! Goodbye!" 
        print(message_to_send)
        broadcast(message_to_send,conn) #notifies all users of exit
        private_broadcast("exit",conn) #notifies the client side that this user is terminating-the actual client thread is closed with the client
    if command[0] == "/id":
        private_broadcast(str(nickname), conn)

def check_valid_len_and_channel(command):
    if len(command) == 1:
        msg = "Must include name of channel"
        private_broadcast(msg, conn)
        return False
    elif list_of_channels.check_valid_channel(command[1]) == False:
        msg = "Channel name not valid"
        private_broadcast(msg, conn)
        return False
    
    return True

def channel_broadcast(message, list_conns, conn):
    for clients in list_conns: 
        try: 
            clients.send(message) 
        except: 
           clients.close() 
           remove(clients) 



def private_broadcast(message, conn):
    for clients in list_of_clients:
        if clients == conn:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 

                remove(clients) 

  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(conn): 
    if conn in list_of_clients: 
        list_of_clients.remove(conn)
        list_of_channels.remove_all_via_conn(conn) 

  
while True: 
  
   
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 

  
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 
  
    #assigns a random nickname to appear on screen-the server keeps track of all the users
    nickname = "User#" + str(randint(100,999))
    #prints the address of the user that just connected 
    print (nickname + " connected")
    list_of_channels.add_user_to_channel("General", nickname, conn)
    
    # creates and individual thread for every user  
    # that connects  
    Thread(target=clientthread, args=(conn, addr, nickname) ).start()



  
conn.close() 
server.close() 