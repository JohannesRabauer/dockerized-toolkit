#!/usr/bin/env python3
"""
Scanned Images Processor

Reconstructs correct page order from double-sided scans,
generates a PDF, and optionally runs OCR via OpenAI.

Environment variables:
  FILENAME       (required) Base name for output files
  MODE           (optional) "full" (default) or "ocr" (OCR only on existing images)
  OPENAI_API_KEY (optional) Enables OCR text extraction
  OPENAI_MODEL   (optional) OpenAI model to use (default: gpt-4o-mini)
"""

import os
import sys
import shutil
import base64
import glob as globmod

DATA_DIR = "/data"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def get_images():
    """Collect and sort image files alphabetically by filename."""
    files = []
    for f in os.listdir(DATA_DIR):
        if f.lower().endswith(IMAGE_EXTENSIONS):
            files.append(f)
    files.sort()
    return files


def interleave_reorder(files):
    """
    Reorder files to reconstruct double-sided scan order.
    Input:  [front1, front2, front3, back3, back2, back1]
    Output: [front1, back1, front2, back2, front3, back3]
    """
    n = len(files)
    mid = (n + 1) // 2
    fronts = files[:mid]
    backs = list(reversed(files[mid:]))

    result = []
    for i in range(mid):
        result.append(fronts[i])
        if i < len(backs):
            result.append(backs[i])
    return result


def rename_files(ordered_files, filename):
    """
    Rename files to {filename}_001.ext, {filename}_002.ext, etc.
    Uses a temp directory to avoid collisions.
    """
    tmp_dir = os.path.join(DATA_DIR, "__tmp_rename")
    os.makedirs(tmp_dir, exist_ok=True)

    # Move to temp dir with new names
    new_paths = []
    for i, f in enumerate(ordered_files, start=1):
        ext = os.path.splitext(f)[1]
        new_name = f"{filename}_{i:03d}{ext}"
        src = os.path.join(DATA_DIR, f)
        tmp = os.path.join(tmp_dir, new_name)
        shutil.move(src, tmp)
        new_paths.append(new_name)

    # Move back to data dir
    for name in new_paths:
        shutil.move(os.path.join(tmp_dir, name), os.path.join(DATA_DIR, name))

    os.rmdir(tmp_dir)
    print(f"Renamed {len(new_paths)} files.")
    return new_paths


def create_pdf(image_files, filename):
    """Create a PDF from the ordered images using img2pdf."""
    import img2pdf

    pdf_path = os.path.join(DATA_DIR, f"{filename}.pdf")
    image_paths = [os.path.join(DATA_DIR, f) for f in image_files]

    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    print(f"Created PDF: {filename}.pdf")


def run_ocr(image_files, filename):
    """Send each image to OpenAI for text recognition."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("Error: OPENAI_API_KEY not set, skipping OCR.")
        return

    from openai import OpenAI

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    client = OpenAI(api_key=api_key)

    print(f"Running OCR with model '{model}'...")
    all_text = []

    for i, img_file in enumerate(image_files, start=1):
        img_path = os.path.join(DATA_DIR, img_file)
        with open(img_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")

        ext = os.path.splitext(img_file)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all text from this scanned document image. "
                                    "Preserve the original structure and formatting as much as possible. "
                                    "Return only the extracted text, no commentary.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{img_data}",
                            },
                        },
                    ],
                }
            ],
        )

        page_text = response.choices[0].message.content
        all_text.append(f"## Page {i}\n\n{page_text}")
        print(f"  Page {i}/{len(image_files)} done.")

    output_path = os.path.join(DATA_DIR, "TEXT_CONTENT.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {filename}\n\n")
        f.write("\n\n---\n\n".join(all_text))
        f.write("\n")

    print("Created TEXT_CONTENT.md")


def main():
    filename = os.environ.get("FILENAME", "").strip()
    if not filename:
        print("Error: FILENAME environment variable not set")
        sys.exit(1)

    mode = os.environ.get("MODE", "full").strip().lower()

    images = get_images()
    if not images:
        print(f"Error: No image files found in {DATA_DIR}")
        sys.exit(1)

    print(f"Found {len(images)} images.")

    if mode == "ocr":
        # OCR only on existing images (already reordered)
        run_ocr(images, filename)
    else:
        # Full pipeline: reorder → rename → PDF → OCR
        ordered = interleave_reorder(images)
        print(f"Reordered: {', '.join(ordered)}")
        renamed = rename_files(ordered, filename)
        create_pdf(renamed, filename)
        run_ocr(renamed, filename)

    print("Done.")


if __name__ == "__main__":
    main()
