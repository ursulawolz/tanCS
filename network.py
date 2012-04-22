#!/usr/bin/env python2

import socket
import ssl
import hashlib
import select
import string

class Message(dict):
    newline = u'\n'
    newlines = (u'\n', u'\r', u'\r\n')
    delimiter = u':'
    specifier = u'/'
    codec = 'utf-8'

    def __init__(self):
        dict.__init__(self)
        self.stream = bytearray()
        self.parse_status = 'ready'
    
    def pull(self, count=0):
        del self.stream[:count]
        return bytes(self.stream)

    def push(self, iterable):
        return self.stream.extend(iterable)

    def complete(self):
        return len(self.stream) == 0

    # Outgoing

    def compose(self):
        self.stream = bytearray()
        self.push(self.action.encode(self.codec))
        self.push(self.newline.encode(self.codec))

        if hasattr(self, 'payload'):
            self[u'length'] = unicode(len(self.payload))

        def write_pair(pair):
            self.push(pair[0].encode(self.codec))
            self.push(self.delimiter.encode(self.codec))
            self.push(pair[1].encode(self.codec))
            self.push(self.newline.encode(self.codec))

        map(write_pair,self.iteritems())

        self.push(u'end'.encode(self.codec))
        self.push(self.newline.encode(self.codec))

        if hasattr(self,'payload'):
            self.push(u'payload:'.encode(self.codec))
            self.push(bytes(self.payload))

    def digest(self, algorithm, content=None, keyword=u'digest'):
        hash_object = hashlib.new(algorithm)
        if content != None:
            hash_object.update(content)
        else:
            hash_object.update(self.payload)
        self[keyword] = algorithm + self.specifier + hash_object.hexdigest()

    # Incoming

    def parse(self):
        payload = False
        action, self.stream = self.stream.split(self.newline.encode(self.codec), 1)
        self.action = unicode(str(action), self.codec)
        while True:
            line, self.stream = self.stream.split(self.newline.encode(self.codec), 1)
            line = unicode(str(line), self.codec)
            if line == u'end':
                break
            keyword, value = line.split(self.delimiter, 1)
            self[keyword] = value
        if u'length' in self:
            self.payload = self.stream.split(self.delimiter.encode(self.codec), 1)[1]


    def verify(self, keyword=u'digest'):
        if keyword not in self or not hasattr(self, 'payload'):
            return False
        
        algorithm, digest = self[keyword].split(self.specifier, 1)
        try:
            hash_object = hashlib.new(algorithm)
        except ValueError:
            return False
        else:
            hash_object.update(self.payload)
            return digest == hash_object.hexdigest().encode(self.codec)

