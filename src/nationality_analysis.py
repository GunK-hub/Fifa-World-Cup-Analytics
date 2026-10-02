import pandas as pd
import plotly.express as px
import streamlit as st


def render_nationality_analysis(
    df,
    nationality_column,
    name_column,
    top_n,
):
    """
    Display performance analysis by nationality.
    """

    st.markdown(
        """
        <div class="section-kicker">
            NATIONALITY ANALYSIS
        </div>

        <div class="section-title">
            How does performance vary by nationality?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if (
        df.empty
        or not nationality_column
        or not name_column
        or "performance_index" not in df.columns
    ):
        st.info(
            "Nationality analysis data is not available."
        )
        return

    analysis_df = df.copy()

    analysis_df["performance_index"] = pd.to_numeric(
        analysis_df["performance_index"],
        errors="coerce",
    )

    analysis_df["goals_scored"] = pd.to_numeric(
        analysis_df["goals_scored"],
        errors="coerce",
    ).fillna(0)

    analysis_df["assists_provided"] = pd.to_numeric(
        analysis_df["assists_provided"],
        errors="coerce",
    ).fillna(0)

    analysis_df = analysis_df.dropna(
        subset=[nationality_column]
    )

    if analysis_df.empty:
        st.info(
            "No nationality data is available."
        )
        return

    nationality_summary = (
        analysis_df
        .groupby(nationality_column)
        .agg(
            Players=(name_column, "nunique"),
            Goals=("goals_scored", "sum"),
            Assists=("assists_provided", "sum"),
            Average_Performance=(
                "performance_index",
                "mean",
            ),
        )
        .reset_index()
    )

    nationality_summary[
        "Average_Performance"
    ] = nationality_summary[
        "Average_Performance"
    ].round(1)

    # Keep nationalities with enough players
    nationality_summary = nationality_summary[
        nationality_summary["Players"] >= 3
    ]

    if nationality_summary.empty:
        st.info(
            "Not enough players per nationality "
            "for a meaningful comparison."
        )
        return

    nationality_summary = (
        nationality_summary
        .sort_values(
            "Average_Performance",
            ascending=False,
        )
        .head(top_n)
    )

    display_df = nationality_summary.rename(
        columns={
            nationality_column: "Nationality",
            "Average_Performance": "Avg Performance Index",
        }
    )

    left, right = st.columns([1.35, 1])

    with left:
        st.dataframe(
            display_df[
                [
                    "Nationality",
                    "Players",
                    "Goals",
                    "Assists",
                    "Avg Performance Index",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        chart_df = display_df.sort_values(
            "Avg Performance Index",
            ascending=True,
        )

        fig = px.bar(
            chart_df,
            x="Avg Performance Index",
            y="Nationality",
            orientation="h",
            title=(
                f"Top {len(display_df)} "
                "nationalities by average index"
            ),
            labels={
                "Avg Performance Index": "Index / 100",
                "Nationality": "",
            },
            color_discrete_sequence=["#D6FF52"],
            text="Avg Performance Index",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            hovertemplate=(
                "%{y}"
                "<br>Average Performance: %{x:.1f}"
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
            key="nationality_performance_analysis",
        )