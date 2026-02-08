# Copilot Instructions for Dockerized Toolkit

## Overview

This repository contains Docker-based utilities to avoid installing software directly on the host machine. Each tool lives in its own subdirectory with a Dockerfile and supporting scripts.

## Build and Test Commands

### YouTube Downloader (YTDL)

Build the image:
```bash
docker build -t ytdl Youtube/
```

Test video download:
```bash
docker run --rm -e MODE=video -e URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v "${PWD}:/downloads" ytdl
```

Test audio download:
```bash
docker run --rm -e MODE=audio -e URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v "${PWD}:/downloads" ytdl
```

### Scanned Images Processor

Build the image:
```bash
docker build -t scansort scanned_images/
```

Process scanned images:
```bash
docker run --rm -e FILENAME="my_document" -v "${PWD}/my_scans:/data" scansort
```

With OCR:
```bash
docker run --rm -e FILENAME="my_document" -e OPENAI_API_KEY -e OPENAI_MODEL="gpt-4o-mini" -v "${PWD}/my_scans:/data" scansort
```

## Architecture

### Project Structure

- Each utility is self-contained in its own directory (e.g., `Youtube/`)
- Each directory contains:
  - `Dockerfile` - Defines the containerized environment
  - Shell script(s) or Python script(s) - Implements the tool's functionality
  - `.gitignore` - Excludes output files (e.g., `*.mp3`, `*.mp4`)

### Tool Pattern

Tools follow a consistent pattern:
1. **Alpine-based images** - Minimal footprint using `python:3-alpine`
2. **Environment variable configuration** - Tools are configured via env vars (e.g., `URL`, `MODE`)
3. **Volume mounting** - Output directory is mounted from the host (`/downloads` or `/data`)
4. **Entrypoint scripts** - Shell or Python scripts handle the tool logic, invoked via `ENTRYPOINT`

### YouTube Downloader Implementation

- Uses `yt-dlp` for downloading
- Requires `ffmpeg` for format conversion
- Modes:
  - `MODE=audio`: Downloads and converts to MP3 (default)
  - `MODE=video`: Downloads best quality MP4 video+audio
- Output filename format: `%(title)s.%(ext)s` (YouTube title + extension)

### Scanned Images Implementation

- Python script (`process.py`) using Pillow, img2pdf, and OpenAI SDK
- Reconstructs double-sided scan order by interleaving fronts and reversed backs
- Uses `img2pdf` for lossless PDF generation (no image re-encoding)
- OCR is optional, triggered by `OPENAI_API_KEY` env var; sends one image per API request
- Volume mount is `/data` (not `/downloads`)

## Conventions

### Adding New Tools

When adding a new dockerized tool:
1. Create a new directory at the repository root
2. Include a `Dockerfile` with Alpine Linux as base (unless specific requirements dictate otherwise)
3. Use environment variables for configuration (not command-line args)
4. Mount `/downloads` as the output directory
5. Add output file patterns to `.gitignore`
6. Update the README.md with usage examples following the existing format

### Dockerfile Practices

- Use `--no-cache` flags for pip/apk to minimize image size
- Set `WORKDIR /downloads` as the standard output location
- Copy and `chmod +x` shell scripts in the build step
- Use `ENTRYPOINT` (not `CMD`) for the main script

### Script Patterns

- Shell scripts use `#!/bin/sh` (not bash) for Alpine compatibility
- Validate required environment variables and exit with clear error messages
- Default to the most common use case when env vars are optional
