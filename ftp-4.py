import socket
import os

BUFFER = 4096
FORMAT = 'utf-8'
SERVER = 'localhost'
PORT = 21

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))

def file_send(path, socket):
    with open(path, 'rb') as file:
        data = file.read(BUFFER)
        while data:
            socket.sendall(data)
            data = file.read(BUFFER)
    file.close()

commands = ['USER ajar\r\n', 'PASS azhar416\r\n', 'TYPE A\r\n', 'PASV\r\n', 'STOR data.txt\r\n', 'QUIT\r\n']
i = 1
while True:
    try:
        if i > len(commands):
            break

        s.send(commands[i-1].encode(FORMAT))
        msg = str(s.recv(BUFFER).decode(FORMAT))
        
        if (msg.__contains__("Entering Passive Mode")):
            msg = msg.split('\r\n')[0].strip()
            p1, p2 = msg.split()[-1].strip('()').split(',')[-2:]
            # print(p1, p2)
            
            new_port = int(p1) * 256 + int(p2)
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.connect((SERVER, new_port))

            file_name = commands[4].strip('\r\n').split()[1]
            path = os.path.join(os.getcwd(), file_name)
            # print(path)

            file_send(path, new_socket)
            new_socket.close()
            msg = str(s.recv(BUFFER).decode(FORMAT))
            print(msg.strip())
        i += 1
                
    except socket.error:
        s.close()
        break
