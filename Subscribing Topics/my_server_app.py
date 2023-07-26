import socket
import sys
import threading

topic_subscribers = {}

def handleClient(client_socket, address):
    client_type = client_socket.recv(1024).decode()
   
    client_type,topic = client_type.split(',')
    if client_type.upper() == "SUBSCRIBER":
       
        if topic not in topic_subscribers:
            topic_subscribers[topic] = []
        topic_subscribers[topic].append(client_socket)
       
        print("Subscriber connected at ", address, " on the topic ", topic)

    elif client_type.upper() == "PUBLISHER":
        if topic not in topic_subscribers:
            topic_subscribers[topic] = []
        topic_subscribers[topic].append(client_socket)
     
        print("A Publisher connected at ", address, " on the topic ", topic)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        topic,message = data.decode().split(':')
        print("Received from publisher at ", address, " : ", message, " --> Topic : ", topic)
        if data.decode().lower() == "terminate":
            break

        if client_type.upper() == "PUBLISHER":
           
            data = message.encode()
            if topic in topic_subscribers:
                subscribers = topic_subscribers[topic]
                for subscriber in subscribers:
                    subscriber.sendall(data)

    if client_type == "SUBSCRIBER":
        topic = client_socket.recv(1024).decode()
        if topic in topic_subscribers:
            topic_subscribers[topic].remove(client_socket)
            print("Subscriber disconnected:", address)
    elif client_type == "PUBLISHER":
        print("Publisher at ", address, " disconnected.")


    client_socket.close()

def setServerConnection(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(100000)
    print("Server listening on port", port)

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handleClient, args=(client_socket, address)).start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Command format should be : python my_server_app.py <port>")
        sys.exit(1)

    else:
        port = int(sys.argv[1])
        setServerConnection(port)
