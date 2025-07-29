# src/op_detector/pipelines/data_engineering/nodes.py

import os
import time
from io import BytesIO

import requests
from PIL import Image

def scrape_images(characters: list, max_results: int, output_dir: str) -> None:
    """
    Scrape up to `max_results` images per character from DuckDuckGo
    and store them under `output_dir/<Character_Name>/`.
    """
    # Lazy‐import the DuckDuckGo client only when this node runs
    from duckduckgo_search import DDGS

    os.makedirs(output_dir, exist_ok=True)

    for name in characters:
        query   = f"One Piece {name}"
        out_dir = os.path.join(output_dir, name.replace(" ", "_"))
        os.makedirs(out_dir, exist_ok=True)

        # 1) Try DuckDuckGo lookup up to 3× with backoff
        image_iter = None
        for attempt in range(1, 4):
            try:
                with DDGS() as ddgs:
                    image_iter = ddgs.images(
                        query,
                        max_results=max_results,
                        timeout=30  # seconds for DDG lookup
                    )
                break
            except Exception as e:
                print(f"⚠️  DDGS lookup attempt {attempt} for '{name}' failed: {e}")
                time.sleep(2 ** attempt)  # exponential backoff: 2s, 4s, 8s

        if image_iter is None:
            print(f"❌ Skipping '{name}' after 3 failed lookups\n")
            continue

        print(f"🕵️  Downloading up to {max_results} images for '{name}'…")
        # 2) Download each image with up to 2 retries
        for i, result in enumerate(image_iter):
            url = result.get("image")
            if not url:
                continue

            for dl_attempt in range(1, 3):
                try:
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    img = Image.open(BytesIO(resp.content)).convert("RGB")
                    img_path = os.path.join(out_dir, f"{name.replace(' ','_')}_{i}.jpg")
                    img.save(img_path)
                    print(f"   ✔️  Saved {img_path}")
                    break
                except Exception as e:
                    print(f"   ✖️  Download attempt {dl_attempt} for '{url}' failed: {e}")
                    time.sleep(1)

            time.sleep(1)  # polite pause between downloads

        print(f"✅ Finished '{name}'\n")
