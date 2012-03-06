import socket
import sys
import ssl
import threading
import time

def f(c):
    question = str(c.recv(1024), 'utf-8')
    print('>', question)
    if question == 'Are you a little teapot?':
        answer = 'Yup, short and stout.'
    else:
        answer = 'No, you must have me mistaken for someone else.'
    time.sleep(5)
    c.send(bytes(answer, 'utf-8'))
    print('<', answer)
    c.close()

print('Hello.')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 31415))
s.listen(5)
ss = ssl.wrap_socket(s, certfile='cert.pem', server_side=True)
for i in range(4):
    c, a = ss.accept()
    t = threading.Thread(target=f, args=(c,))
    t.start()
ss.close()
print('Goodbye.')
