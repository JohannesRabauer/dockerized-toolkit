FROM python:3-alpine

# Install image processing dependencies
RUN apk add --no-cache \
        zlib-dev \
        libjpeg-turbo-dev \
    && pip install --no-cache-dir \
        Pillow \
        img2pdf \
        openai

WORKDIR /data

COPY process.py /usr/local/bin/process.py
RUN chmod +x /usr/local/bin/process.py

ENTRYPOINT ["python", "/usr/local/bin/process.py"]
