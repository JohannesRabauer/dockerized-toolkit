# Copilot Instructions for Dockerized Toolkit

Docker-based utilities that avoid installing software on the host. Each tool is self-contained in its own subdirectory with a Dockerfile and scripts.

## Build and Test Commands

```bash
# YouTube Downloader
docker build -t ytdl Youtube/
docker run --rm -e MODE=video -e URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v "${PWD}:/downloads" ytdl
docker run --rm -e MODE=audio -e URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v "${PWD}:/downloads" ytdl

# Scanned Images Processor
docker build -t scansort scanned_images/
docker run --rm -e FILENAME="my_document" -v "${PWD}/my_scans:/data" scansort
docker run --rm -e FILENAME="my_document" -e REORDER=false -v "${PWD}/my_scans:/data" scansort
docker run --rm -it -e FILENAME="my_document" -e OPENAI_API_KEY -e OPENAI_MODEL="gpt-4o-mini" -v "${PWD}/my_scans:/data" scansort
docker run --rm -it -e FILENAME="my_document" -e MODE=ocr -e OPENAI_API_KEY -v "${PWD}/my_scans:/data" scansort

# MP3 Extractor
docker build -t mp3extract mp3_extractor/
docker run --rm -e INPUT="video.mp4" -v "${PWD}:/downloads" mp3extract
```

All build commands run from the repo root. There are no automated tests — verify by building the image and running it.

## Architecture

- **One directory per tool** at the repo root, each containing a `Dockerfile`, script(s), and `.gitignore`
- **No shared code** between tools — each is fully independent
- **No docker-compose** — tools are standalone `docker run` commands
- **Config via env vars only** — no CLI args, no config files
- **Volume-mounted output** — containers write to a mounted dir, never embed output in the image

Reference implementations: `Youtube/` (shell-based tool), `scanned_images/` (Python-based tool)

## Code Style

### Shell Scripts (see `Youtube/downloader.sh`)
- `#!/bin/sh` — POSIX-only, no bashisms (Alpine has no bash)
- Linear flow, no functions needed for simple tools
- Validate required env vars at the top: `if [ -z "$VAR" ]; then echo "Error: ..."; exit 1; fi`

### Python Scripts (see `scanned_images/process.py`)
- `#!/usr/bin/env python3`
- Structured with functions and a `main()` entry point
- Constants at module level (e.g., `DATA_DIR`, `IMAGE_EXTENSIONS`)
- `print(msg, flush=True)` for real-time Docker log output
- `sys.exit(1)` on fatal errors with descriptive messages
- Third-party imports at the top; use standard library where possible
- No type hints currently used
- Retry with exponential backoff for external API calls

## Conventions

### Adding New Tools

1. Create a new directory at the repository root
2. Include a `Dockerfile` using `python:3-alpine` base (unless requirements dictate otherwise)
3. Use environment variables for configuration — not command-line args
4. Set `WORKDIR` to the output mount point (prefer `/downloads`)
5. Add a `.gitignore` for output file patterns
6. Update `README.md` with usage examples following the existing format

### Dockerfile Pattern (consistent order)

```dockerfile
FROM python:3-alpine
RUN apk add --no-cache <system-deps> \
    && pip install --no-cache-dir <python-deps>
WORKDIR /downloads
COPY script.sh /usr/local/bin/script.sh
RUN chmod +x /usr/local/bin/script.sh
ENTRYPOINT ["/usr/local/bin/script.sh"]
```

Key rules: `--no-cache` on all install commands, `ENTRYPOINT` (not `CMD`), scripts go in `/usr/local/bin/`.

### .gitignore Strategy

- Root `.gitignore`: repo-level artifacts (`/temp`, `__pycache__`)
- Per-tool `.gitignore`: output artifacts (`*.mp3`, `*.mp4`, `*.pdf`, etc.)

### Known Inconsistency

The `scanned_images/` tool mounts at `/data` instead of the standard `/downloads`. New tools should use `/downloads`.
