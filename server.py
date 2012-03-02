import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 31415))
s.listen(1)
c, a = s.accept()
s.shutdown(socket.SHUT_RDWR)
s.close()

question = str(c.recv(4096),'utf-8')
print('>', question)
if question == 'Are you a little teapot?':
    answer = 'Yup, short and stout.'
else:
    answer = 'No, you must have me mistaken for someone else.'
c.send(bytes(answer, 'utf-8'))
print('<', answer)
c.close()
