import pandas as pd
import plotly.express as px
import streamlit as st


CORRELATION_METRICS = {
    "goals_scored": "Goals",
    "assists_provided": "Assists",
    "dribbles_per_90": "Dribbles / 90",
    "interceptions_per_90": "Interceptions / 90",
    "tackles_per_90": "Tackles / 90",
    "total_duels_won_per_90": "Duels Won / 90",
    "performance_index": "Performance Index",
}


def render_correlation_analysis(df):
    """
    Display correlations between player performance metrics.
    """

    st.markdown(
        """
        <div class="section-kicker">
            CORRELATION ANALYSIS
        </div>

        <div class="section-title">
            Which metrics move together?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("Correlation analysis data is not available.")
        return

    available_columns = [
        column
        for column in CORRELATION_METRICS
        if column in df.columns
    ]

    if len(available_columns) < 2:
        st.info(
            "Not enough performance metrics are available "
            "for correlation analysis."
        )
        return

    correlation_df = df[available_columns].copy()

    for column in available_columns:
        correlation_df[column] = pd.to_numeric(
            correlation_df[column],
            errors="coerce",
        )

    correlation_matrix = correlation_df.corr()

    correlation_matrix = correlation_matrix.rename(
        index=CORRELATION_METRICS,
        columns=CORRELATION_METRICS,
    )

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Performance Metric Correlations",
        labels={
            "x": "Metric",
            "y": "Metric",
            "color": "Correlation",
        },
    )

    fig.update_layout(
        height=600,
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="performance_correlation_matrix",
    )

    st.caption(
        "Correlation ranges from -1 to +1. "
        "Values closer to +1 indicate a stronger positive relationship, "
        "while values closer to -1 indicate a stronger negative relationship."
    )