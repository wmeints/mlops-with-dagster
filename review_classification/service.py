from typing import List

import bentoml
from bentoml.io import NumpyNdarray, Text

vectorizer = bentoml.sklearn.get("text_vectorizer:latest").to_runner()
classifier = bentoml.sklearn.get("reviews_classifier_rf:latest").to_runner()

svc = bentoml.Service("review_classifier", runners=[vectorizer, classifier])


@svc.api(input=Text(), output=NumpyNdarray())  # type: ignore
async def classify_review(text: str) -> List[float]:
    vector = await vectorizer.async_run(text)
    prediction = await classifier.async_run(vector)

    return prediction
