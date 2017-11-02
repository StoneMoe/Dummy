# Dummy
A tiny fully dynamic telegram bot framework, simple and naive.
# Quick Setup
0.Create a new bot via @BotFather

1.Edit config.py

2.Configure your Web Server like:

	location / {
		proxy_pass http://127.0.0.1:8081;
		proxy_set_header X-Forwarded-For $remote_addr
	}
3.Start your Dummy System:

	# pip install Flask requests MySQL-Python
	# python dummy.py
	
4.Enjoy