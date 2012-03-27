#!/usr/bin/env python

class Account(object):
	def __init__(self,acctid,uname,password,avatar=-1,projects=-1,groups=-1):
		self.acctid = acctid
		self.uname = uname
		self.password = password
		self.avatar = avatar
		self.projects = projects
		self.groups = groups