from dagster import define_asset_job

from review_classification.assets import data as data_assets
from review_classification.assets import model as model_assets

train_model_job = define_asset_job(
    "train_model",
    [
        data_assets.raw_reviews,
        data_assets.classification_features,
        model_assets.text_vectorizer,
        model_assets.random_forest_classifier,
    ],
)
