#!/usr/bin/env python

class Comment(object):
	def __init__(self,text,time,acct,proj,rev,filename,line=-1):
		self.text = text
		self.time = time
		self.acct = acct
		self.proj = proj
		self.rev = rev
		self.filename = filename
		self.line = line

	def getText(self):
		return self.text

	def getTime(self):
		return self.time

	def getName(self):
		return self.acct.getName()