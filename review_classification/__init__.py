from dagster import Definitions

from review_classification.assets.data import (classification_features,
                                               raw_reviews)
from review_classification.assets.model import (random_forest_classifier,
                                                text_vectorizer)
from review_classification.jobs import train_model_job

module_assets = [
    raw_reviews,
    classification_features,
    text_vectorizer,
    random_forest_classifier,
]

module_jobs = [train_model_job]

defs = Definitions(assets=module_assets, jobs=module_jobs)
