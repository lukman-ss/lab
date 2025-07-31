"""
This is a boilerplate pipeline 'scraping'
generated using Kedro 1.0.0
"""
# src/anti_fatigue_detector/pipelines/scraping/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import scrape_images

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=scrape_images,
            inputs=dict(
                events="params:scraping.events",
                max_results="params:scraping.max_results",
                raw_images_dir="params:scraping.raw_images_dir",
                lookup_timeout="params:scraping.lookup_timeout",
                download_timeout="params:scraping.download_timeout",
                polite_pause="params:scraping.polite_pause"
            ),
            outputs=None,
            name="scraping_node"
        )
    ])
