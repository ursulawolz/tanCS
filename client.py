import socket
import sys

if len(sys.argv) != 2:
    sys.exit()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 31415))

question = 'Are you a little teapot?'
print('<', question)
s.send(bytes(question, 'utf-8'))
answer = str(s.recv(4096),'utf-8')
print('>', answer)
s.close()
