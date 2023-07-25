import socket
import sys
import threading

subscribers = []
publishers = []

def handle_client(client_socket, address):
    client_type = client_socket.recv(1024).decode()

    if client_type.upper() == "SUBSCRIBER":
        subscribers.append(client_socket)
        print("Subscriber connected on:", address)
    elif client_type.upper() == "PUBLISHER":
        publishers.append(client_socket)
        print("Publisher connected on:", address)

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print("Received from publisher at", address, ":", data.decode())
        if data.decode().lower() == "terminate":
            break

        if client_type.upper() == "PUBLISHER":
            for subscriber in subscribers:
                subscriber.sendall(data)

    if client_type.upper() == "SUBSCRIBER":
        subscribers.remove(client_socket)
        print("Subscriber at " + address + " disconnected:")
    elif client_type.upper() == "PUBLISHER":
        publishers.remove(client_socket)
        print("Publisher at " + address + " disconnected:")
    client_socket.close()



def setServerConnection(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(100000)
    print("Server listening on port", port)

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Command format should be : python my_server_app.py <port>")
        sys.exit(1)

    else: 
        port = int(sys.argv[1])
        setServerConnection(port)
