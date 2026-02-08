# Dockerized Toolkit

Here are some docker commands i keep using instead of installing some software.

## YTDL

1. `docker build -t ytdl .`
2. Video: `docker run --rm -e MODE=video -e URL="https://www.youtube.com/watch?v=XYZ" -v "${PWD}:/downloads" ytdl`
3. Audio: `docker run --rm -e MODE=audio -e URL="https://www.youtube.com/watch?v=XYZ" -v "${PWD}:/downloads" ytdl`

## Scanned Images

Reconstructs correct page order from double-sided scans, creates a PDF, and optionally extracts text via OpenAI OCR.

1. `docker build -t scansort scanned_images/`
2. `docker run --rm -e FILENAME="my_document" -v "${PWD}/my_scans:/data" scansort`
3. With OCR: `docker run --rm -it -e FILENAME="my_document" -e OPENAI_API_KEY -v "${PWD}/my_scans:/data" scansort`

Environment variables:
- `FILENAME` (required) — base name for renamed files and the output PDF
- `OPENAI_API_KEY` (optional) — passed through from host system; enables OCR text extraction to `TEXT_CONTENT.md`
- `OPENAI_MODEL` (optional) — OpenAI model to use (default: `gpt-4o-mini`)
- `MODE` (optional) — `full` (default) runs the complete pipeline; `ocr` runs only OCR on existing images