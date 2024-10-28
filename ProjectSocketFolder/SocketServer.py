# IMPORTS
import socket
from multiprocessing import Process
import time

# GLOBAL VARIABLES
IP_MAIN = socket.gethostbyname(socket.gethostname()) # IP of local machine
LOOPBACK_IP = '127.0.0.1'

HOST = IP_MAIN
PORT = 26512
SIZE = 1024
HEADER =- 64
FORMAT = 'utf-8'

disconnect_msg = "/end"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows reuse of address (Test)
s.bind((HOST, PORT))

def clientHandle(conn, addr):
    print(f'<<< NEW CONNECTION >>> {addr} has been connected.')
        
    connect = True
    while connect:
        data_length = conn.recv(SIZE).decode(FORMAT)
            
        if not data_length:
            print('Issue occured. Check connection and/or data.')
            break
            
        if data_length:
            data_length = int(data_length)
            data = conn.recv(data_length).decode(FORMAT)
                
            if data == disconnect_msg:
                connect = False
                break
                
            print(f'<<< TEST >>> {addr}: {data}')
        
    s.close()
        
def start():
    s.listen()
    print(f'Server listening on port: {PORT}')
        
    while True:
        conn, addr = s.accept()
            
        process = Process(target=clientHandle, args=(conn, addr))
            
        #st = time.time()
            
        process.start()
        #process.join()
            
        ##et = time.time()
        #(f'Time: {et-st}')
    
            
if __name__ == '__main__':
    print('<<< STARTING SERVER >>>')
    start()