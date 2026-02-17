FROM python:3-alpine
RUN apk add --no-cache ffmpeg
WORKDIR /downloads
COPY extract.sh /usr/local/bin/extract.sh
RUN chmod +x /usr/local/bin/extract.sh
ENTRYPOINT ["/usr/local/bin/extract.sh"]
