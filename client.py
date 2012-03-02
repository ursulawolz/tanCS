import socket
import sys
import ssl

if len(sys.argv) != 2:
    sys.exit()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss = ssl.wrap_socket(s)
ss.connect((sys.argv[1], 31415))

question = 'Are you a little teapot?'
print('<', question)
ss.send(bytes(question, 'utf-8'))
answer = str(ss.recv(4096),'utf-8')
print('>', answer)
ss.close()
