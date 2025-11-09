#!/bin/sh
# Environment variables:
# URL  = YouTube URL
# MODE = "audio" or "video" (default audio)

if [ -z "$URL" ]; then
    echo "Error: URL environment variable not set"
    exit 1
fi

if [ "$MODE" = "video" ]; then
    # Download best mp4 video+audio
    yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" -o "/downloads/%(title)s.%(ext)s" "$URL"
else
    # Default: extract mp3 audio
    yt-dlp -x --audio-format mp3 -o "/downloads/%(title)s.%(ext)s" "$URL"
fi
