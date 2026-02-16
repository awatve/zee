#!/usr/bin/env python3
import requests
import sys
import datetime
import os
import hashlib

URL = "https://mini.allinonereborn.fun/zee_paid/index.php?id=0-9-zeemarathi"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"
}

def get_final_url():
    try:
        r = requests.get(URL, headers=HEADERS, allow_redirects=True, timeout=20)
        r.raise_for_status()
        return r.url
    except Exception as e:
        print(f"Error following redirect: {e}", file=sys.stderr)
        sys.exit(2)


def compute_file_hash(path):
    if not os.path.isfile(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    final = get_final_url()
    print(f"Final URL: {final}")

    old_hash = compute_file_hash("index.html")
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zee Marathi → Direct link</title>
  <style>
    body {{font-family:system-ui,sans-serif; text-align:center; padding:3rem; background:#f9f9f9; color:#111;}}
    h1 {{color:#222;}}
    .box {{background:white; padding:2rem; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.08); max-width:90%; margin:2rem auto;}}
    a {{color:#0066cc; font-size:1.3rem; word-break:break-all; text-decoration:none;}}
    a:hover {{text-decoration:underline;}}
    .meta {{color:#666; font-size:0.95rem; margin-top:2rem;}}
  </style>
</head>
<body>
  <h1>Direct link (updated {now})</h1>
  <div class="box">
    <p><strong>Final destination:</strong></p>
    <p><a href="{final}" target="_blank" rel="noopener noreferrer">{final}</a></p>
  </div>
  <p class="meta">Automatically checked & updated daily via GitHub Actions</p>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    new_hash = compute_file_hash("index.html")

    if old_hash == new_hash:
        print("URL has not changed → no commit needed")
        sys.exit(0)
    else:
        print("URL changed → should commit")
        sys.exit(1)


if __name__ == "__main__":
    main()
