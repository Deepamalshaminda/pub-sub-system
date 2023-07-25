import socket
import sys

def setClientConnection(server_ip, port, client_type):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server as a " + client_type +". Type 'terminate' to exit.")

    client_socket.sendall(client_type.encode())

    if client_type.upper() == "SUBSCRIBER":
        while True:
            data = client_socket.recv(1024)
            if data.lower() == "terminate":
                break
            if not data:
                break
            
            print("Received message:", data.decode())

    elif client_type.upper() == "PUBLISHER":
        while True:
            message = input()
            client_socket.sendall(message.encode())
            if message.lower() == "terminate":
                break

    else : print("Invalid client tpye. Client type should be 'SUBCSRIBER' OR 'PUBLISHER'")

    client_socket.close()
    print("Disconnected from server")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Command format should be : python my_client_app.py <server_ip> <port> <client_type (PUBLISHER or SUBSCRIBER)>")
        print("If server runs on localhost please use 127.0.0.1 as the server IP")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    client_type = sys.argv[3]

    setClientConnection(server_ip, port, client_type)