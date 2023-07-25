import socket
import sys

def setClientConnection(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server. Type 'terminate' to exit.")

    while True:
        message = input()
        client_socket.sendall(message.encode())
        if message.lower() == "terminate":
            break

    client_socket.close()
    print("Server connection closed succesfully.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Command format should be: python my_client_app.py <server_ip> <server_port>")
        print("If server runs on localhost please use 127.0.0.1 as the server IP")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    setClientConnection(server_ip, port)
