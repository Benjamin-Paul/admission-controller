FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 443

CMD ["python3", "server.py"]