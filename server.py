import socket
import sys
import ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 31415))
s.listen(1)
ss = ssl.wrap_socket(s, certfile='cert.pem', server_side=True)
c, a = ss.accept()
ss.close()

question = str(c.recv(4096),'utf-8')
print('>', question)
if question == 'Are you a little teapot?':
    answer = 'Yup, short and stout.'
else:
    answer = 'No, you must have me mistaken for someone else.'
c.send(bytes(answer, 'utf-8'))
print('<', answer)
c.close()
