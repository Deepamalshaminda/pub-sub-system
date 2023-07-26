import socket
import sys

def setClientConnection(server_ip, port, client_type, topic=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print("Connected to server as a " + client_type +" on " + topic+ " topic. Type 'terminate' to exit.")

    client_socket.sendall(client_type.encode())

    if client_type.upper() == "SUBSCRIBER":
        if topic:
            topic = f',{topic}'
            client_socket.sendall(topic.encode())
        else:
            print("Please provide a topic for the subscriber.")
            client_socket.close()
            return

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received message:", data.decode())

    elif client_type.upper() == "PUBLISHER":
        if topic:
            topicTobesend = f',{topic}'
            client_socket.sendall(topicTobesend.encode())
        else:
            print("Please provide a topic for the publisher.")
            client_socket.close()
            return

        while True:
            message = input("Enter message : ")
            prepareforsend = f'{topic}:{message}'
            client_socket.sendall(prepareforsend.encode())
            if message == "terminate":
                break

    client_socket.close()
    print("Disconnected from server")

if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python my_client_app.py <server_ip> <port> <client_type (PUBLISHER or SUBSCRIBER)> [<topic>]")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    client_type = sys.argv[3]
    topic = sys.argv[4] if len(sys.argv) == 5 else None

    setClientConnection(server_ip, port, client_type, topic)
