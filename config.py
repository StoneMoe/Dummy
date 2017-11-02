#!/usr/bin/env python
# coding:utf-8


class Config(object):
    # bot
    botNickname = ""
    botUsername = ""  # without @
    botMasterID = 0  # Use /userid command
    botToken = ""
    # webhook URL
    webhookURL = "/%s" % botToken
    # API URL
    apiURL = "https://api.telegram.org/bot%s/" % botToken
    # Public URL: For photo upload, Telegram server will download file via http
    publicURL = "https://example.com/public/"
    publicPath = "/path/to/example.com/public/"
