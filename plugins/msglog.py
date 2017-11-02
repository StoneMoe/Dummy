#!/usr/min/env python
# coding:utf-8
import time

priority = 0


def plugin_load():
	pass


def plugin_main(update):
	if not update.IS_MESSAGE and not update.IS_EDITEDMESSAGE:
		raise NotImplementedError("msglog recv not support message type")  # only support message and edited_message yet

	m = update.msg

	logText = "[c%s][m%s]" % (
		m.chat.id,  # chat id
		m.id  # msg id
	)
	logText += "[%s]%s%s%s(u%s):" % (
		m.chat._dict["type"],  # chat type text
		"[%s]" % (m.chat.title[:7] + ".." if len(m.chat.title) > 9 else m.chat.title) if not m.chat.IS_PRIVATE else "",  # chat title if not private
		m.sender.nickname[:7] + ".." if len(m.sender.nickname) > 9 else m.sender.nickname,  # nick
		"(@%s)" % m.sender.username if m.sender.username else "",  # username
		m.sender.id  # user id
	)

	# Let's find supported message types
	contents = [key[4:].lower().title() for key, value in update.msg.__dict__.items() if key[:4] == "HAS_" and value is True]
	# print {key: value for key, value in update.msg.__dict__.items() if key[:4] == "HAS_"}

	if update.IS_EDITEDMESSAGE:
		logText += "[Edit]"
	if m.forwarded:
		logText += "[Forward]"
	if m.reply:
		logText += "[Re:%s]" % m.reply.id
	if contents != ["Text"]:  # if just contain text than hide type tag
		logText += "[%s]" % ",".join(contents)
	if "Text" in contents:
		logText += m._dict["text"].replace("\n", "")
	if "Caption" in contents:
		logText += "(%s)" % m.caption

	screen(logText)


def screen(text):
	print("[%s]%s" % (time.strftime("%Y/%m/%d %H:%M:%S"), text))


if __name__ == "__main__":
	print("This is a dummy plugin.")
