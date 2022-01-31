FROM python:3.8

COPY . /

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  chmod 777 /main.py