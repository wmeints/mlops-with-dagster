from pathlib import Path

import pandas as pd
from dagster import AssetExecutionContext, Output, asset


@asset
def raw_reviews(context: AssetExecutionContext) -> Output[str]:
    input_path = Path("data/source/reviews.json")
    output_path = Path(f"data/raw/{str(context.run_id)}/reviews.parquet")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_source = pd.read_json(input_path, lines=True)
    df_source.to_parquet(output_path)

    metadata = dict(num_records=len(df_source), columns=list(df_source.columns))

    return Output(str(output_path), metadata=metadata)


@asset
def classification_features(
    context: AssetExecutionContext, raw_reviews: str
) -> Output[str]:
    input_path = Path(raw_reviews)
    output_path = Path(f"data/preprocessed/{str(context.run_id)}/features.parquet")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_source = pd.read_parquet(input_path)
    df_output = df_source[["reviewText", "vote"]]
    df_output = df_output.dropna()

    df_output.to_parquet(output_path)

    return Output(str(output_path))
