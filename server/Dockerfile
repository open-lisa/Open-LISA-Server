FROM python:3.8

COPY . /

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get update -y && \
    chmod +x /main.py

ENTRYPOINT ["/bin/sh"]