import sys
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

if len(sys.argv) != 2:
    sys.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(6)
ss = ssl.wrap_socket(s)
ss.connect((sys.argv[1], 31415))

question = etree.Element('question')
question.text = 'Are you a little teapot?' 
print('tx:' + str(etree.tostring(question), 'utf-8'))
ss.send(etree.tostring(question, encoding='utf-8'))
answer = etree.fromstring(str(ss.recv(1024), 'utf-8'))
print('rx:' + str(etree.tostring(answer), 'utf-8'))
ss.close()
