# SSL/TLS Documentation

## Table of Contents

<!-- toc -->

- [Overview](#overview)
- [Flask Secure Connection](#Flask-Secure-Connection)
- [Fast Api Secure Connection](#Fast-Api-Secure-Connection)
- [Nginx](#Nginx)
<!-- tocstop -->

## Overview
This documentation is for anyone trying to setup a secure connection in Flask, FastApi, Spark, Airflow, 

## Flask Secure Connection
As an example, we're going to use the application [app.py](https://github.com/KubeHawk/SSL/blob/main/Flask/app.py).

```sh
# Import flask module
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'Hello to Flask!'
 
# main driver function
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',ssl_context=('cert.pem','key.pem'))
```
For the certificates, we only need to generate both cert.pem and key.pem with OpenSSL.

```sh
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
This command will generate the certificate we need with RSA algorithme using a 4096 bit and expires in a year.

In order to perform the same work through a container, we just have to containerize our application with the [Dockerfile](https://github.com/KubeHawk/SSL/blob/main/Flask/Dockerfile).

```sh
FROM python:3-alpine
 
# Create app directory
WORKDIR /app
 
# Install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
# Bundle app source
COPY . .
 
EXPOSE 5000
EXPOSE 443
EXPOSE 80
CMD [ "python3", "app.py"]
```

```sh
docker build -t flask .
```
```sh
docker run -p 5000:5000 flask
```

![image](https://github.com/KubeHawk/SSL/assets/75808939/993ce510-a9ab-4028-a1de-61fbbe19ebc7)

## Fast Api Secure Connection
As an example, we're going to use the application [app.py](https://github.com/KubeHawk/SSL/blob/main/Fast-Api/app.py).

```sh
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_main():
    return {"message" : "Hello World of FastAPI HTTPS"}
```
To start the server we use uvicorn with the [server.py](https://github.com/KubeHawk/SSL/blob/main/Fast-Api/server.py).

```sh
import uvicorn
if __name__ == '__main__':
    uvicorn.run("app:app",host="0.0.0.0",port=8432,reload=True,ssl_keyfile="key.pem",ssl_certfile="cert.pem")
```
For the certificates, we only need to generate both cert.pem and key.pem with OpenSSL.

```sh
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

In order to perform the same work through a container, we just have to containerize our application with the [Dockerfile](https://github.com/KubeHawk/SSL/blob/main/Fast-Api/Dockerfile).

![image](https://github.com/KubeHawk/SSL/assets/75808939/5f49df70-cac7-4a1c-b55a-208979cde00d)

```sh
FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8432
EXPOSE 80
EXPOSE 443
CMD ["python3", "server.py"]
```

```sh
docker build -t fast-api .
```
```sh
docker run -p 8432:8432 fast-api
```

## Nginx

To use Nginx over Https we only have to configure the server to listen on port 443 with ssl and export the certificate and the key into the configuration file.
in the default site-available add these 3 lines.

```sh
 listen 443 ssl;
 ssl_certificate /etc/nginx/ssl/nginx.crt;
 ssl_certificate_key /etc/nginx/ssl/nginx.key;
```
After that, the configuration file should look like this.

```sh
##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# https://www.nginx.com/resources/wiki/start/
# https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
# https://wiki.debian.org/Nginx/DirectoryStructure
#
# In most cases, administrators will remove this file from sites-enabled/ and
# leave it as reference inside of sites-available where it will continue to be
# updated by the nginx packaging team.
#
# This file will automatically load configuration files provided by other
# applications, such as Drupal or Wordpress. These applications will be made
# available underneath a path with that package name, such as /drupal8.
#
# Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
##

# Default server configuration
#
server {
	listen 80 default_server;
	listen [::]:80 default_server;
 listen 443 ssl;
	# SSL configuration
	#
	# listen 443 ssl default_server;
	# listen [::]:443 ssl default_server;
	#
	# Note: You should disable gzip for SSL traffic.
	# See: https://bugs.debian.org/773332
	#
	# Read up on ssl_ciphers to ensure a secure configuration.
	# See: https://bugs.debian.org/765782
	#
	# Self signed certs generated by the ssl-cert package
	# Don't use them in a production server!
	#
	# include snippets/snakeoil.conf;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	ssl_certificate /etc/nginx/ssl/nginx.crt;
 ssl_certificate_key /etc/nginx/ssl/nginx.key;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}

	# pass PHP scripts to FastCGI server
	#
	#location ~ \.php$ {
	#	include snippets/fastcgi-php.conf;
	#
	#	# With php-fpm (or other unix sockets):
	#	fastcgi_pass unix:/run/php/php7.4-fpm.sock;
	#	# With php-cgi (or other tcp sockets):
	#	fastcgi_pass 127.0.0.1:9000;
	#}

	# deny access to .htaccess files, if Apache's document root
	# concurs with nginx's one
	#
	#location ~ /\.ht {
	#	deny all;
	#}
}


# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
#server {
#	listen 80;
#	listen [::]:80;
#
#	server_name example.com;
#
#	root /var/www/example.com;
#	index index.html;
#
#	location / {
#		try_files $uri $uri/ =404;
#	}
#}
```
