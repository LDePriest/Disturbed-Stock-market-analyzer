# IMPORTS
import socket
from multiprocessing import Process, Queue
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

def clientHandle(conn, addr, queue):
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
            
            queue.put((addr, data))
            print(f'<<< TEST >>> {addr}: {data}')
    
    conn.close()
    print(f'<<< LOST CONNECTION >>> {addr} has been disconnected.')

# Process from the queue
def processQ(queue):
    while True:
        if not queue.empty():
            addr, data = queue.get()
            
            if data == disconnect_msg:
                print("<< TERMINATION >>")
                break

            print(f"Processing data from {addr}: {data}")
        time.sleep(1)

def start():
    s.listen()
    print(f'Server listening on port: {PORT}')
        
    queue = Queue()
    process = Process(target=processQ, args=(queue,))
    process.start()
    
    while True:
        try:
            conn, addr = s.accept()
            Cprocess = Process(target=clientHandle, args=(conn, addr, queue))
                
            Cprocess.start()
            #process.join()
        except Exception as e:
            #Cprocess.close()
            print(f'Error detected: {e}')
            
if __name__ == '__main__':
    print('<<< STARTING SERVER >>>')
    start()