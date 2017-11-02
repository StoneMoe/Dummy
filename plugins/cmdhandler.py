#!/usr/bin/env python
# coding:utf-8
import random
import sys

from config import Config

priority = 1

commandReg = {
}


def plugin_load():
	global commandReg, plt
	commandReg = {name[4:]: getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__]) if name[:4] == "aux_"}


def plugin_main(update):
	global commandReg
	# Only deal with normal text message
	if not update.IS_MESSAGE or not update.msg.HAS_TEXT or not update.msg.text:
		return
	msg = update.msg

	isCommand = True if msg.text[0] == "/" else False
	isValid   = True if isCommand and len(msg.text) > 1 and msg.text[1:].split()[0] in commandReg else False

	if isCommand:
		if isValid and (msg.IS_MENTIONED or msg.chat.IS_PRIVATE):  # response to commands in private chat or mentioned in group chat
			update.handled = True
			return commandReg[msg.text[1:].split()[0]](update, msg.text[1:].split()[1:])
		elif msg.chat.IS_PRIVATE or msg.IS_MENTIONED:
			update.handled = True
			return "Maybe you need some /help%s" % ("@" + Config.botUsername if msg.chat.IS_GROUP or msg.chat.IS_SUPERGROUP else "")
		else:
			return


def aux_start(update, args):
	return "Hi. /help%s" % ("@" + Config.botUsername if update.msg.chat.IS_GROUP or update.msg.chat.IS_SUPERGROUP else "")


def aux_roll(update, args):
	if args:
		limit = args[0]
	else:
		limit = 100
	try:
		maxset = int(limit)
		return "%s rolls %s point(s)" % (update.msg.sender.nickname, str(random.randint(1, maxset)))
	except Exception:
		return "Limit need a integer"


def aux_userid(update, args):
	return str(update.msg.sender.id)


def aux_help(update, args):
	helptext = """
/help - Get help
/userid - Get my user id
/roll [limit] - Roll a dice"""
	return helptext


if __name__ == "__main__":
	print("This is a dummy plugin.")
