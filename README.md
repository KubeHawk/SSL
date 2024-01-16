# SSL/TLS Documentation

## Table of Contents

<!-- toc -->

- [Overview](#overview)
- [Flask Secure Connection](#Flask-Secure-Connection)
- [Fast Api Secure Connection](#Fastapi-Secure-Connection)
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
