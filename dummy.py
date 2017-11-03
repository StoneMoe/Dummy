#!/usr/bin/env python
# coding:utf-8
from flask import Flask, request, Response
import json
import os
import sys
import time
import traceback
import logging

import api
from config import Config
from model import Update

app = Flask(__name__)
app.debug = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Env
reload(sys)
sys.setdefaultencoding('UTF8')
os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()  # Unix only
sys.dont_write_bytecode = True

# Plugin
print("Loading plugins...")
sys.path.append(os.getcwd() + '/plugins')
plugins = []
for file in os.listdir("./plugins"):
    filename = file.split('.')[0]
    plugin = __import__(filename)
    plugins.append(plugin)
plugins.sort(key=lambda x: x.priority)
for plugin in plugins:
    plugin.plugin_load()  # Respect priority
print("EventLoop Order: " + ",".join([p.__name__ for p in plugins]))


@app.route("/")
def index():
    return "Running"


@app.route(Config.webhookURL, methods=['POST'])
def webhookEntry():
    try:
        jsonResult = eventLoop(request.data)
        # print(json.dumps(json.loads(request.data), indent=4).decode("unicode-escape"))
        if jsonResult:
            return Response(jsonResult, mimetype='application/json')
        else:
            return ""
    except Exception:
        requestInfo   = json.dumps(json.loads(request.data), indent=4).decode("unicode-escape")
        callstackInfo = traceback.format_exc()
        print requestInfo
        print callstackInfo
        return Response(
            api.sendMessage(
                Config.botMasterID,
                "<strong>Error</strong>\nRaw:\n<code>%s</code>\n\nTraceback:\n<code>%s</code>" % (requestInfo, callstackInfo),
                isReturn=True),
            mimetype='application/json')


def eventLoop(jraw):
    update = Update(jraw)
    # EventLoop
    for plugin in plugins:
        reply = plugin.plugin_main(update)
        if update.handled:
            return api.sendMessage(update.msg.chat.id, reply, isReturn=True)


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8081)
    print("Use uWSGI.")
