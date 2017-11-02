#!/usr/bin/env python
# coding:utf-8

"""
This is a example that show you basic plugin structure
"""

priority = 100  # bigger number, lower priority


def plugin_load():
	# We'll call plugin_load() ONCE after import this file immediately
	pass


def plugin_main(update):
	pass
	# When dummy core recv a update, it will start a eventloop to notify all plugins one by one ordered by priority
	# --- case1. Just Do something...
	# dosth()
	# --- and without return
	#
	# --- case2. if you want to reply to msg source directly
	# update.handled = True
	# return "something wanna reply"
	#
	# --- NOTICE
	# 1. Set 'update.handled = True' will stop eventloop after this function return, this means further plugins behind will not be triggered
	# 2. return is not necessary, dummy core will handle empty results.
	# 3. if you want to reply directly, Set 'update.handled = True' is necessary, otherwise you need to use a API request to send message.


if __name__ == "__main__":
	print("This is a dummy plugin.")
