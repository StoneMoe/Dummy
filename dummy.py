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
app.debug = True
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
def index():  # We have a XSS here.
    return """
<h1 style="color:red">Server Error in "/" Application</h1><br>
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '\"""" + request.headers.get("X-Forwarded-For") + """\")' at line 1
"""


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
        requestInfo   = json.dumps(json.loads(request.data), indent=4, sort_keys=False).decode("unicode-escape")
        callstackInfo = traceback.format_exc()
        print requestInfo
        print callstackInfo
        return Response(
            api.sendMessage(
                Config.botMasterID,
                "<strong>Error</strong>\nRaw:\n<code>%s</code>\n\nTraceback:\n<code>%s</code>" % (requestInfo, callstackInfo),
                isResponse=True),
            mimetype='application/json')


def eventLoop(jraw):
    update = Update(jraw)
    # EventLoop
    for plugin in plugins:
        reply = plugin.plugin_main(update)
        if update.handled:
            return api.sendMessage(update.msg.chat.id, reply, isResponse=True)


if __name__ == "__main__":
    print("Starting Flask...")
    app.run(host='127.0.0.1', port=8081)
