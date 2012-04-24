#!/usr/bin/env python2 import select
import socket
import ssl
import hashlib
import collections
import string

class Message(dict):
    newline = u'\n'
    delimiter = u':'
    specifier = u'/'
    codec = 'utf-8'

    def __init__(self):
        dict.__init__(self)
        self.queue = collections.deque()
    
    def pull(self, count=0):
        if count >= len(self.queue):
            self.queue.clear()
        else:
            def remove(value):
                self.queue.popleft()
            map(remove,xrange(count))
        
        return b''.join(self.queue)

    def push(self, iterable):
        return self.queue.extend(iterable)

    def complete(self):
        return len(self.queue) == 0

    # Outgoing

    def compose(self):
        self.queue.clear()
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
        if not hasattr(self, '_parse_mode'):
            self._parse_mode = 'action'

        if self._parse_mode == 'action':
            line = self.getline()
            if line == None:
                return False
            self.action = line
            self._parse_mode = 'keywords'

        while self._parse_mode == 'keywords':
            line = self.getline()
            if line == None:
                return False
            else:
                if self.delimiter.encode(self.codec) in line:
                    keyword, value = line.split(
                            self.delimiter.encode(self.codec), 1)
                    self[keyword] = value
                elif line == u'end':
                    if u'length' in self:
                        self._parse_mode = 'ready'
                    else:
                        self._parse_mode = 'complete'

        while self._parse_mode == 'ready':
            try:
                element = self.queue.popleft()
            except IndexError:
                return False
            if element == self.delimiter.encode(self.codec):
                self._payload_queue = collections.deque()
                self._parse_mode = 'payload'

        while self._parse_mode == 'payload':
            if len(self._payload_queue) == int(self[u'length']):
                self.payload = b''.join(self._payload_queue)
                del self._payload_queue
                self._parse_mode = 'complete'
            else:
                try:
                    self._payload_queue.append(self.queue.popleft())
                except IndexError:
                    return False

        if self._parse_mode == 'complete':
            del self._parse_mode
            return True

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

    def getline(self):
        lf = u'\n'.encode(self.codec)
        cr = u'\r'.encode(self.codec)
        content = False

        if lf in self.queue or cr in self.queue:
            line = collections.deque()
            while True:
                try:
                    element = self.queue.popleft()
                except IndexError:
                    return None
                if element == lf or element == cr:
                    if content:
                        return unicode(b''.join(line), self.codec)
                else:
                    line.append(element)
                    if not content:
                        if lf in self.queue or cr in self.queue:
                            content = True
                        else:
                            self.queue.appendleft(element)
                            return None
        else:
            return None

class Error(Exception):
    def __init__(self, message=u'An unknown error occured.'):
        self.message = message

    def __str__(self):
        return str(self.message)

    def __unicode__(self):
        return unicode(self.message)

