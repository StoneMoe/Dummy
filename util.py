#!/usr/bin/env python
# coding:utf-8
import MySQLdb
import time
import random
import string


class DB(object):
	"""DB Class"""
	def __init__(self, host, user, passwd, database):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.database = database
		try:
			self.conn = MySQLdb.connect(
				host=self.host,
				user=self.user,
				passwd=self.passwd,
				db=self.database
			)
			self.db = self.conn.cursor()
		except Exception as e:
			print("Error occured while connecting to database: " + str(e))
			raise

	def do(self, sql, param):
		try:
			self.db.execute(sql, param)
			self.conn.commit()
		except Exception as e:
			print("Error occured while log a update: " + str(e))
			print(self.db._last_executed)


def randomString(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))


def publicUniFilename():
	return str(int(time.time())) + randomString(5)
