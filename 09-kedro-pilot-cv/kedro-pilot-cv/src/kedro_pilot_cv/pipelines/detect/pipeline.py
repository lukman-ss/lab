# src/kedro_pilot_cv/pipelines/detect/pipeline.py
from kedro.pipeline import Pipeline, node
from .nodes import vertical_scroll_hand


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=vertical_scroll_hand,
                inputs=[
                    "params:model_path",
                    "params:scroll_threshold",      # ← renamed here
                    "params:scroll_sensitivity",
                ],
                outputs=None,
                name="vertical_scroll_hand_node",
            )
        ]
    )
