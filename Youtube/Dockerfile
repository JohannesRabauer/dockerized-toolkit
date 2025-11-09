FROM python:3-alpine

# Install yt-dlp and ffmpeg
RUN apk add --no-cache ffmpeg \
    && pip install --no-cache-dir yt-dlp

WORKDIR /downloads

# Use a small wrapper script inside the container
COPY downloader.sh /usr/local/bin/downloader.sh
RUN chmod +x /usr/local/bin/downloader.sh

ENTRYPOINT ["/usr/local/bin/downloader.sh"]