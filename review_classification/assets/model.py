from pathlib import Path

import joblib
import mlflow
import pandas as pd
from dagster import Output, asset
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


@asset
def text_vectorizer(classification_features: str) -> Output[str]:
    df_features = pd.read_parquet(classification_features)

    vectorizer = TfidfVectorizer()
    vectorizer.fit(df_features["reviewText"])

    output_path = Path("models/vectorizer.pkl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        joblib.dump(vectorizer, f)

    return Output(str(output_path))


@asset
def random_forest_classifier(classification_features: str, text_vectorizer: str):
    df_features = pd.read_parquet(classification_features)

    with open(text_vectorizer, "rb") as f:
        vectorizer = joblib.load(f)

    df_train, df_test = train_test_split(df_features, test_size=0.2)

    X_train = vectorizer.transform(df_train["reviewText"])  # type: ignore
    y_train = df_train["vote"]  # type: ignore

    X_test = vectorizer.transform(df_test["reviewText"])  # type: ignore
    y_test = df_test["vote"]  # type: ignore

    with mlflow.start_run():
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)

        score = classifier.score(X_test, y_test)

        output_path = Path("models/classifier.pkl")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        mlflow.sklearn.log_model(classifier, "models")
        mlflow.log_metric("accuracy", score)  # type: ignore

    with open(output_path, "wb") as f:
        joblib.dump(classifier, f)

    return Output(str(output_path))
