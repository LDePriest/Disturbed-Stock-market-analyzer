import socket

HOST = "127.0.0.1" #loopback IP address, change when needed
PORT = 5500 # Port number, change if needed
SIZE = 1024 # Default size

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(5) # listen for 5 or less connections, this will be the default setting
    
    connect, address = s.accept()
    
    with connect:
        print(f"Connected from {address} has been made.")
        
        while True:
            data = connect.recv(SIZE).decode()
            if not data:
                print('Issue with data or connection. Check Issue.')
                break
            print(f'Received from {address}: {data}')
            connect.sendall(data.encode())
    
    connect.close()
    print(f'Connection with {address} has been closed.')