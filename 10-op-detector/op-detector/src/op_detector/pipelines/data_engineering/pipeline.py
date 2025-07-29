# src/op_detector/pipelines/data_engineering/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import scrape_images

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=scrape_images,
            inputs=dict(
                characters="params:characters",
                max_results="params:max_results",
                output_dir="params:raw_images_dir"
            ),
            outputs=None,
            name="data_engineering_scrape_images",
        )
    ])
