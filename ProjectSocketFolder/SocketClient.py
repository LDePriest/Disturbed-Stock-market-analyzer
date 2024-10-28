# IMPORTS
import socket

# GLOBAL VARIABLES
IP_MAIN = socket.gethostbyname(socket.gethostname()) # IP of local machine
LOOPBACK_IP = '127.0.0.1'

HOST = IP_MAIN
PORT = 26512
SIZE = 1024
HEADER = 64
FORMAT = 'utf-8'

disconnect_msg = "/end"

def clientStart():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        try:
            c.connect((HOST,PORT))
            print(f'<<< CONNECTION >>> Connection to server at {HOST}: {PORT}')
            
            while True:
                message = input("Enter your message to send: ")
                
                if message == disconnect_msg:
                    print('Disconnecting from server...')
                    dataSend(c, message)
                    break
            
                dataSend(c, message)
                
                data = c.recv(SIZE)
                print(f" <<< RECEIVED >>> {data.decode(FORMAT)}")
            
        except ConnectionRefusedError:
            print('Connection refused. Check to see if server is running.')
        except Exception as e:
            print(f"Error occured: {e}")
            
    c.close()

def dataSend(c, data):
        data_msg = data.encode(FORMAT)
        data_length = len(data_msg)
        send_length = str(data_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        
        c.send(send_length)
        c.send(data_msg)

if __name__ == '__main__':
    clientStart()