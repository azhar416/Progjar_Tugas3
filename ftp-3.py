import socket

BUFFER = 4096
FORMAT = 'utf-8'
SERVER = 'localhost'
PORT = 21

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))

commands = ['USER ajar\r\n', 'PASS azhar416\r\n', 'TYPE I\r\n', 'PASV\r\n','MLSD\r\n', 'QUIT\r\n']
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

            s.send(commands[i-1+1].encode(FORMAT))
            file = new_socket.recv(BUFFER).decode(FORMAT)
            while file:
                file_list = file.split('\r\n')[:-1]
                for j in file_list:
                    file_name = j.split(';')[-1].strip()
                    print(file_name)
                file = new_socket.recv(BUFFER).decode(FORMAT)
        i += 1
                
    except socket.error:
        s.close()
        break
