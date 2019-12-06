# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
closed = False 
#IP_address = input("What is the IP address of the server you're connecting to?")
Port = 6667

#if len(sys.argv) != 3: 
#     print ("Correct usage: script, IP address, port number")
#     exit() 
IP_address = str(sys.argv[1]) 
#Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 


while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
    if closed == True: #if our flag to close is set, we break the while loop
        break

    
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print(message)
            check_for_close = message.split()
            if check_for_close == []: #If the server screws up, it sends empty messages
                print("SERVER ERROR!! Disconnecting from server")
                closed = True
                break
            if check_for_close[0] == "exit": #If the server tells us to close, we set out flag to close
                closed = True
                break
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.flush() 
server.close()