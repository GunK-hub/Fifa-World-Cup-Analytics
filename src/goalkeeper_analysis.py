import pandas as pd


GOALKEEPER_METRICS = {
    "save_percentage": "Save Percentage",
    "clean_sheets": "Clean Sheets",
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
        (series - min_value)
        / (max_value - min_value)
    )


def calculate_goalkeeper_index(
    df,
    position_column="position",
):
    """
    Calculate a goalkeeper-specific performance index.

    The index uses goalkeeper-specific metrics:
    - Save percentage
    - Clean sheets

    The result is calculated only for GK players.
    """

    result = df.copy()

    if position_column not in result.columns:
        return result

    result["goalkeeper_index"] = pd.NA

    goalkeeper_mask = (
        result[position_column] == "GK"
    )

    normalized_columns = []

    for metric in GOALKEEPER_METRICS:

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

        normalized_columns.append(
            normalized_column
        )

    if normalized_columns:
        result.loc[
            goalkeeper_mask,
            "goalkeeper_index",
        ] = (
            result.loc[
                goalkeeper_mask,
                normalized_columns,
            ]
            .mean(axis=1)
            * 100
        )

    result["goalkeeper_index"] = (
        pd.to_numeric(
            result["goalkeeper_index"],
            errors="coerce",
        )
        .round(1)
    )

    return result

def render_goalkeeper_analysis(
    goalkeeper_df,
    name_column,
    position_column,
    top_n,
):
    """
    Display goalkeeper-specific performance analysis.
    """

    import plotly.express as px
    import streamlit as st

    st.markdown(
        '<div class="section-kicker">GOALKEEPER ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            Which goalkeepers stand out?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if (
        goalkeeper_df.empty
        or not name_column
        or "goalkeeper_index" not in goalkeeper_df.columns
    ):
        st.info(
            "Goalkeeper analysis data is not available."
        )
        return

    gk_df = goalkeeper_df[
        goalkeeper_df[position_column] == "GK"
    ].copy()

    gk_df["goalkeeper_index"] = pd.to_numeric(
        gk_df["goalkeeper_index"],
        errors="coerce",
    )

    gk_df = (
        gk_df
        .dropna(subset=["goalkeeper_index"])
        .sort_values(
            "goalkeeper_index",
            ascending=False,
        )
        .head(top_n)
        .copy()
    )

    if gk_df.empty:
        st.info("No goalkeeper data is available.")
        return

    gk_df.insert(
        0,
        "Rank",
        range(1, len(gk_df) + 1),
    )

    display_columns = [
        "Rank",
        name_column,
    ]

    if "save_percentage" in gk_df.columns:
        display_columns.append("save_percentage")

    if "clean_sheets" in gk_df.columns:
        display_columns.append("clean_sheets")

    display_columns.append("goalkeeper_index")

    display_df = gk_df[display_columns].rename(
        columns={
            name_column: "Player",
            "save_percentage": "Save %",
            "clean_sheets": "Clean Sheets",
            "goalkeeper_index": "Goalkeeper Index",
        }
    )

    left, right = st.columns([1.35, 1])

    with left:
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    with right:
        chart_df = display_df.sort_values(
            "Goalkeeper Index",
            ascending=True,
        )

        fig = px.bar(
            chart_df,
            x="Goalkeeper Index",
            y="Player",
            orientation="h",
            title=(
                f"Top {len(display_df)} "
                "goalkeepers by index"
            ),
            labels={
                "Goalkeeper Index": "Index / 100",
                "Player": "",
            },
            color_discrete_sequence=["#83C8E8"],
            text="Goalkeeper Index",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            hovertemplate=(
                "%{y}"
                "<br>Goalkeeper Index: %{x:.1f}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=420,
            margin=dict(
                l=10,
                r=20,
                t=60,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="goalkeeper_performance_index",
        )