import sys
import threading
import time
import socket
import ssl
try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        import xml.etree.ElementTree as etree

def f(c):
    question = etree.fromstring(str(c.recv(1024), 'utf-8'))
    print('rx:' + str(etree.tostring(question), 'utf-8'))
    answer = etree.Element('answer')
    if question.text == 'Are you a little teapot?':
        answer.text = 'Yup, short and stout.'
    else:
        answer.text = 'No, you must have me mistaken for someone else.'
    time.sleep(5)
    c.send(etree.tostring(answer, encoding='utf-8'))
    print('tx:' + str(etree.tostring(answer), 'utf-8'))
    c.close()

print('info:Hello.')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname(), 31415))
s.listen(5)
for i in range(4):
    c, a = s.accept()
    ss = ssl.wrap_socket(c, certfile='cert.pem', server_side=True)
    ss.settimeout(5)
    t = threading.Thread(target=f, args=(ss,))
    t.start()
s.shutdown(socket.SHUT_RDWR)
s.close()
print('info:Goodbye.')
