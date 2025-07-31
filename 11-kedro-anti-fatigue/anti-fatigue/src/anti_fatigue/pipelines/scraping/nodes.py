# src/anti_fatigue_detector/pipelines/scraping/nodes.py

import os
import time
from io import BytesIO

import requests
from PIL import Image

def scrape_images(
    events: list,
    max_results: int,
    raw_images_dir: str,
    lookup_timeout: int,      # we’ll use this for our own backoff if desired
    download_timeout: int,
    polite_pause: float
) -> None:
    """
    For each event in `events`, scrape up to `max_results` images via DuckDuckGo,
    saving them under `raw_images_dir/<event>/`.
    """
    # Lazy‐import the DuckDuckGo client, handling either package name:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        from ddgs import DDGS  # fallback if you installed ddgs

    os.makedirs(raw_images_dir, exist_ok=True)

    for evt in events:
        safe_name = evt.replace(" ", "_")
        out_dir = os.path.join(raw_images_dir, safe_name)
        os.makedirs(out_dir, exist_ok=True)
        print(f"🕵️  Scraping '{evt}' → {out_dir} …")

        # 1) Query DuckDuckGo (no unsupported timeout param)
        try:
            with DDGS() as ddgs:
                image_iter = ddgs.images(
                    evt,
                    max_results=max_results
                )
        except Exception as e:
            print(f"⚠️  Failed lookup '{evt}': {e}")
            continue

        # 2) Download each image
        for i, result in enumerate(image_iter):
            url = result.get("image") or result.get("thumbnail")
            if not url:
                continue
            try:
                resp = requests.get(url, timeout=download_timeout)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                fname = f"{safe_name}_{i}.jpg"
                img.save(os.path.join(out_dir, fname))
                print(f"   ✔️  {fname}")
            except Exception as e:
                print(f"   ✖️  Skipping #{i} for '{evt}': {e}")
            time.sleep(polite_pause)

        print(f"✅ Finished scraping '{evt}'\n")
