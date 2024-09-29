import socket

HOST = '127.0.0.1'
PORT = 5500
SIZE = 1024

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print(f'Connection to server at {HOST}: {PORT}')
    
    try:
        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            response = s.recv(SIZE).decode()
            print(f"Response from server: {response}")
    finally:
        s.close
        print("Connection closed.")