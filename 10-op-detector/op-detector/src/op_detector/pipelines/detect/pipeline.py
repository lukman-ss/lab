"""
This is a boilerplate pipeline 'detect'
generated using Kedro 1.0.0
"""

# src/op_detector/pipelines/detect/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import detect_op_character

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=detect_op_character,
            inputs=dict(
                image_path="params:detect.image_path",
                model_path="params:train.model_output"
            ),
            outputs=None,
            name="detect_op_node"
        )
    ])
