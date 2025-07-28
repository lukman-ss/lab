"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

# Import your detect pipeline factory
from kedro_pilot_cv.pipelines.detect.pipeline import create_pipeline as detect_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines."""
    pipelines = find_pipelines()
    pipelines["detect"] = detect_pipeline()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
