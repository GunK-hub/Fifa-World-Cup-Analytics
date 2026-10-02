import pandas as pd


def calculate_statistical_insights(
    df,
    name_column,
    position_column,
    nationality_column,
):
    """
    Calculate key statistical insights from the player dataset.
    """

    insights = {}

    if df.empty:
        return insights

    analysis_df = df.copy()

    # Convert important metrics to numeric
    numeric_columns = [
        "goals_scored",
        "assists_provided",
        "dribbles_per_90",
        "interceptions_per_90",
        "tackles_per_90",
        "total_duels_won_per_90",
        "performance_index",
    ]

    for column in numeric_columns:
        if column in analysis_df.columns:
            analysis_df[column] = pd.to_numeric(
                analysis_df[column],
                errors="coerce",
            )

    # --------------------------------
    # Top scorer
    # --------------------------------

    if (
        name_column
        and name_column in analysis_df.columns
        and "goals_scored" in analysis_df.columns
    ):
        scorer_df = analysis_df.dropna(
            subset=["goals_scored"]
        )

        if not scorer_df.empty:
            top_scorer = scorer_df.loc[
                scorer_df["goals_scored"].idxmax()
            ]

            insights["top_scorer"] = {
                "player": str(top_scorer[name_column]),
                "value": float(top_scorer["goals_scored"]),
            }

    # --------------------------------
    # Top assister
    # --------------------------------

    if (
        name_column
        and name_column in analysis_df.columns
        and "assists_provided" in analysis_df.columns
    ):
        assister_df = analysis_df.dropna(
            subset=["assists_provided"]
        )

        if not assister_df.empty:
            top_assister = assister_df.loc[
                assister_df["assists_provided"].idxmax()
            ]

            insights["top_assister"] = {
                "player": str(top_assister[name_column]),
                "value": float(
                    top_assister["assists_provided"]
                ),
            }

    # --------------------------------
    # Highest performance index
    # --------------------------------

    if (
        name_column
        and name_column in analysis_df.columns
        and "performance_index" in analysis_df.columns
    ):
        index_df = analysis_df.dropna(
            subset=["performance_index"]
        )

        if not index_df.empty:
            top_performer = index_df.loc[
                index_df["performance_index"].idxmax()
            ]

            insights["top_performer"] = {
                "player": str(top_performer[name_column]),
                "value": float(
                    top_performer["performance_index"]
                ),
            }

    # --------------------------------
    # Highest dribbler
    # --------------------------------

    if (
        name_column
        and name_column in analysis_df.columns
        and "dribbles_per_90" in analysis_df.columns
    ):
        dribble_df = analysis_df.dropna(
            subset=["dribbles_per_90"]
        )

        if not dribble_df.empty:
            top_dribbler = dribble_df.loc[
                dribble_df["dribbles_per_90"].idxmax()
            ]

            insights["top_dribbler"] = {
                "player": str(top_dribbler[name_column]),
                "value": float(
                    top_dribbler["dribbles_per_90"]
                ),
            }

    # --------------------------------
    # Position averages
    # --------------------------------

    if (
        position_column
        and position_column in analysis_df.columns
    ):
        position_metrics = [
            "goals_scored",
            "assists_provided",
            "dribbles_per_90",
            "tackles_per_90",
        ]

        available_metrics = [
            column
            for column in position_metrics
            if column in analysis_df.columns
        ]

        if available_metrics:
            position_summary = (
                analysis_df
                .groupby(position_column)[available_metrics]
                .mean()
                .round(2)
            )

            insights["position_summary"] = position_summary

    # --------------------------------
    # Nationality averages
    # --------------------------------

    if (
        nationality_column
        and nationality_column in analysis_df.columns
    ):
        nationality_summary = (
            analysis_df
            .groupby(nationality_column)
            .agg(
                Players=(name_column, "count"),
                Goals=("goals_scored", "sum"),
                Assists=("assists_provided", "sum"),
            )
            .sort_values(
                "Goals",
                ascending=False,
            )
            .head(10)
        )

        insights["nationality_summary"] = (
            nationality_summary
        )

    return insights