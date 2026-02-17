#!/bin/sh
if [ -z "$INPUT" ]; then
    echo "Error: INPUT environment variable not set"
    echo "Usage: docker run --rm -e INPUT=\"video.mp4\" -v \"\${PWD}:/downloads\" mp3extract"
    exit 1
fi

if [ ! -f "/downloads/$INPUT" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

BITRATE="${BITRATE:-192k}"
OUTPUT="$(echo "$INPUT" | sed 's/\.[^.]*$//')".mp3

echo "Extracting audio from: $INPUT"
echo "Bitrate: $BITRATE"

ffmpeg -i "/downloads/$INPUT" -vn -ab "$BITRATE" -y "/downloads/$OUTPUT" 2>&1

echo "Created: $OUTPUT"
