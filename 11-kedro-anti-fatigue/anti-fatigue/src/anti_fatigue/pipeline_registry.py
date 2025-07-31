from kedro.pipeline import Pipeline
from .pipelines.scraping.pipeline import create_pipeline as create_scraping
from .pipelines.train.pipeline    import create_pipeline as create_train
from .pipelines.detect.pipeline   import create_pipeline as create_detect

def register_pipelines() -> dict[str, Pipeline]:
    scraping = create_scraping()
    training = create_train()
    detecting= create_detect()
    return {
        "__default__": scraping + training + detecting,
        "scraping":    scraping,
        "train":       training,
        "detect":      detecting,
    }
