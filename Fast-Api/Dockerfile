FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8432
EXPOSE 80
EXPOSE 443
CMD ["python3", "server.py"]
