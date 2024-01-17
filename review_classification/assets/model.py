from pathlib import Path

import bentoml
import joblib
import mlflow
import pandas as pd
from dagster import Output, asset
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


@asset
def text_vectorizer(classification_features: str) -> Output[None]:
    df_features = pd.read_parquet(classification_features)

    vectorizer = TfidfVectorizer()
    vectorizer.fit(df_features["reviewText"])

    bentoml.sklearn.save_model("text_vectorizer", vectorizer)

    return Output(None)


@asset(deps=[text_vectorizer])
def random_forest_classifier(classification_features: str) -> Output[None]:
    vectorizer = bentoml.sklearn.load_model("text_vectorizer:latest")

    df_features = pd.read_parquet(classification_features)
    df_train, df_test = train_test_split(df_features, test_size=0.2)

    X_train = vectorizer.transform(df_train["reviewText"])  # type: ignore
    y_train = df_train["vote"]  # type: ignore

    X_test = vectorizer.transform(df_test["reviewText"])  # type: ignore
    y_test = df_test["vote"]  # type: ignore

    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)

    score = classifier.score(X_test, y_test)

    bentoml.sklearn.save_model(
        "reviews_classifier_rf", classifier, metadata={"accuracy": score}
    )

    return Output(None)
