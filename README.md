# Dummy
A tiny fully dynamic telegram bot framework, simple and naive.

# Quick Setup Example
0.Create a new bot via @BotFather

1.Edit config.py

2.Start your Dummy System:

	# pip install Flask requests MySQL-Python uwsgi
	# cd /path/to/git/root
	# uwsgi --ini uwsgi.ini

3.Configure your Web Server like:

	location / {
		uwsgi_pass unix:///tmp/dummysys.sock;
		include uwsgi_params;
	}
	
	location /public {
		root /path/to/git/root;
	}

and reload it

	# sudo systemctl reload nginx

4.Enjoy