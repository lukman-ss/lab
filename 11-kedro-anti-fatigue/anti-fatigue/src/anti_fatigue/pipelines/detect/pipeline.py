# src/anti_fatigue_detector/pipelines/detect/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import detect_and_record

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=detect_and_record,
            inputs=dict(
                video_source="params:detect.video_source",
                eye_closed_frames="params:detect.eye_closed_frames",
                yawn_frames="params:detect.yawn_frames",
                scale_factor_eye="params:detect.scale_factor_eye",
                min_neighbors_eye="params:detect.min_neighbors_eye",
                scale_factor_smile="params:detect.scale_factor_smile",
                min_neighbors_smile="params:detect.min_neighbors_smile",
                record_dir="params:detect.record_dir",
                pre_buffer_secs="params:detect.pre_buffer_secs",
                post_record_secs="params:detect.post_record_secs"   # <-- corrected key
            ),
            outputs=None,
            name="detect_and_record_node",
        )
    ])
