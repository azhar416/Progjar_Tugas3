import socket

BUFFER = 1024
FORMAT = 'utf-8'
SERVER = 'localhost'
PORT = 21

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))

commands = ['USER ajar\r\n', 'PASS azhar416\r\n', 'PWD\r\n', 'QUIT\r\n']
i = 1
while True:
    try:
        if i > len(commands):
            break

        s.send(commands[i-1].encode(FORMAT))
        msg = str(s.recv(BUFFER).decode(FORMAT))
        
        if (commands[i-1].__contains__('USER')):
            msg = msg.split('\r\n')[0]
            msg = msg.split('-')
            msg = ' '.join(msg)

        print(msg.strip())
        i += 1
                
    except socket.error:
        s.close()
        break
