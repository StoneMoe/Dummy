#!/usr/bin/env python
# coding:utf-8
import requests
import json

from config import Config


def sendMessage(chatID, text, parseMode="HTML", disableWebpagePreview=True, isResponse=False):
	if not text:
		return ""
	data = {
		"chat_id": chatID,
		"text": text,
		"parse_mode": parseMode,
		"disable_web_page_preview": disableWebpagePreview
	}
	if isResponse:
		data["method"] = "sendMessage"
		return json.dumps(data)
	requests.post(Config.apiURL + "sendMessage", params=data)


def sendPhoto(chatID, publicFilename, caption="", disableNotify=False, replyMsgID=None):
	data = {
		"chat_id": chatID,
		"photo": Config.publicURL + publicFilename,
		"caption": caption,
		"disable_notification": disableNotify
	}
	if replyMsgID:
		data["reply_to_message_id"] = replyMsgID
	requests.post(Config.apiURL + "sendPhoto", params=data)
