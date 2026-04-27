#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import sys
import argparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
visited_pages = set()


def is_valid_image(url):
    path = urlparse(url).path.lower()
    return path.endswith(ALLOWED_EXTENSIONS)


def get_filename(url):
    path = urlparse(url).path
    name = os.path.basename(path)

    if not name:
        return None

    return name


def save_image(img_url, folder):
    try:
        response = requests.get(
            img_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            print(f"[FAIL] {img_url} ({response.status_code})")
            return

        filename = get_filename(img_url)

        if not filename:
            return

        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"[OK] {filename}")

    except requests.exceptions.RequestException:
        print(f"[ERROR] {img_url}")


def crawl(url, folder, recursive=False, level=5):
    if url in visited_pages:
        return

    if level < 0:
        return

    visited_pages.add(url)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            print(f"[HTTP ERROR] {response.status_code} - {url}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Download images
        for img in soup.find_all("img"):
            src = img.get("src")

            if not src:
                continue

            img_url = urljoin(url, src)

            if is_valid_image(img_url):
                save_image(img_url, folder)

        # Recursive mode
        if recursive and level > 0:
            for link in soup.find_all("a"):
                href = link.get("href")

                if not href:
                    continue

                next_url = urljoin(url, href)

                if next_url.startswith("http"):
                    crawl(
                        next_url,
                        folder,
                        recursive=True,
                        level=level - 1
                    )

    except requests.exceptions.RequestException:
        print(f"[ERROR] {url}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        action="store_true",
        help="recursive download"
    )

    parser.add_argument(
        "-l",
        type=int,
        default=5,
        help="maximum depth level"
    )

    parser.add_argument(
        "-p",
        default="./data/",
        help="save path"
    )

    parser.add_argument(
        "url",
        help="target URL"
    )

    args = parser.parse_args()

    os.makedirs(args.p, exist_ok=True)

    crawl(
        args.url,
        args.p,
        recursive=args.r,
        level=args.l
    )


if __name__ == "__main__":
    main()