# src/op_detector/pipelines/train/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import train_model

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=train_model,
            inputs=dict(
                raw_images_dir="params:train.raw_images_dir",
                model_output="params:train.model_output",
                epochs="params:train.epochs"
            ),
            outputs=None,
            name="train_model_node"
        )
    ])
