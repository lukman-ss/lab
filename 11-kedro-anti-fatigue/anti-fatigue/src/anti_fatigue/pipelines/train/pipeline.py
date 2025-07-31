"""
This is a boilerplate pipeline 'train'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Pipeline, node
from .nodes import train_model

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=train_model,
            inputs=dict(
                raw_images_dir="params:train.raw_images_dir",
                model_output="params:train.model_output",
                epochs="params:train.epochs",
                batch_size="params:train.batch_size",
                learning_rate="params:train.learning_rate"
            ),
            outputs=None,
            name="train_model_node",
        )
    ])
