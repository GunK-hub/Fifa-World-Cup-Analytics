import pandas as pd


POSITION_METRICS = {
    "FW": [
        "goals_scored",
        "assists_provided",
        "dribbles_per_90",
        "total_duels_won_per_90",
    ],
    "MF": [
        "assists_provided",
        "dribbles_per_90",
        "interceptions_per_90",
        "tackles_per_90",
        "total_duels_won_per_90",
    ],
    "DF": [
        "interceptions_per_90",
        "tackles_per_90",
        "total_duels_won_per_90",
    ],
}


def min_max_normalize(series):
    series = pd.to_numeric(
        series,
        errors="coerce",
    ).fillna(0)

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(
            0.0,
            index=series.index,
        )

    return (
        series - min_value
    ) / (
        max_value - min_value
    )


def calculate_position_index(
    df,
    position_column="position",
):
    result = df.copy()

    if position_column not in result.columns:
        return result

    result["position_index"] = pd.NA

    for position, metrics in POSITION_METRICS.items():

        position_mask = (
            result[position_column] == position
        )

        normalized_metrics = []

        for metric in metrics:

            if metric not in result.columns:
                continue

            normalized_column = (
                f"{metric}_normalized"
            )

            result[normalized_column] = (
                min_max_normalize(
                    result[metric]
                )
            )

            normalized_metrics.append(
                normalized_column
            )

        if normalized_metrics:

            result.loc[
                position_mask,
                "position_index",
            ] = (
                result.loc[
                    position_mask,
                    normalized_metrics,
                ]
                .mean(axis=1)
                * 100
            )

    result["position_index"] = (
        pd.to_numeric(
            result["position_index"],
            errors="coerce",
        )
        .round(1)
    )

    return result