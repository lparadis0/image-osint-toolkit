#!/usr/bin/env python3

import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS


ALLOWED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp"
)


def is_valid_file(filename):
    return filename.lower().endswith(ALLOWED_EXTENSIONS)


def print_separator():
    print("-" * 50)


def show_basic_info(filepath):
    print(f"File: {filepath}")
    print(f"Size: {os.path.getsize(filepath)} bytes")


def show_image_info(img):
    print(f"Format: {img.format}")
    print(f"Width: {img.width}")
    print(f"Height: {img.height}")
    print(f"Mode: {img.mode}")


def show_exif(img):
    exif_data = img.getexif()

    if not exif_data:
        print("No EXIF metadata found")
        return

    print("EXIF Metadata:")

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag}: {value}")


def analyze_image(filepath):
    print_separator()

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    if not is_valid_file(filepath):
        print(f"[ERROR] Unsupported file: {filepath}")
        return

    try:
        with Image.open(filepath) as img:
            show_basic_info(filepath)
            show_image_info(img)
            show_exif(img)

    except Exception:
        print(f"[ERROR] Cannot open file: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        return

    for filepath in sys.argv[1:]:
        analyze_image(filepath)


if __name__ == "__main__":
    main()