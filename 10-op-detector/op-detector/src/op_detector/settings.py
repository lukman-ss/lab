# src/op_detector/settings.py

CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        "parameters": [
            "parameters.yml",
            "parameters_data_engineering.yml",
            "parameters_train.yml",
            "parameters_detect.yml"
        ],
        "catalog":     ["catalog*.yml"],
        "credentials": ["credentials*.yml"],
        "logging":     ["logging*.yml"],
        "metrics":     ["metrics*.yml"]
    }
}

from .pipelines import (
    data_engineering as de,
    train           as tr,
    detect          as det
)

PIPELINE_REGISTRY = {
    "__default__":       de.create_pipeline() + tr.create_pipeline() + det.create_pipeline(),
    "data_engineering":  de.create_pipeline(),
    "train":             tr.create_pipeline(),
    "detect":            det.create_pipeline(),
}
