import socket

# Server configuration (replace '127.0.0.1' with the actual server IP address)
HOST = '127.0.0.1'
PORT = 65432

def main():
    stock_symbols = input("Enter stock symbols separated by commas: ")
    
    # Set up the client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        # Send stock symbols to the server
        client_socket.sendall(stock_symbols.encode())

        # Receive and print the analysis result from the server
        data = client_socket.recv(1024)
        print("Received analysis:", data.decode())

if __name__ == "__main__":
    main()
