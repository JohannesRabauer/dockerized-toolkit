# Dockerized Toolkit

Here are some docker commands i keep using instead of installing some software.

## YTDL

1. `docker build -t ytdl .`
2. Video: `docker run --rm -e MODE=video -e URL="https://www.youtube.com/watch?v=XYZ" -v "${PWD}:/downloads" ytdl`
3. Audio: `docker run --rm -e MODE=audio -e URL="https://www.youtube.com/watch?v=XYZ" -v "${PWD}:/downloads" ytdl`