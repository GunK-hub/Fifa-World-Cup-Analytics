import pandas as pd
import plotly.express as px
import streamlit as st


def render_goals_assists_scatter(df):
    """
    Display the relationship between goals and assists.
    """

    st.markdown(
        """
        <div class="section-kicker">ATTACKING ANALYSIS</div>
        <div class="section-title">
            Goals vs Assists
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No player data is available.")
        return

    # Create a separate dataframe for the chart
    plot_df = df.copy()

    # Convert goals and assists to numeric values
    plot_df["Goals"] = pd.to_numeric(
        plot_df["goals_scored"],
        errors="coerce",
    )

    plot_df["Assists"] = pd.to_numeric(
        plot_df["assists_provided"],
        errors="coerce",
    )

    # Remove rows where goals or assists are missing
    plot_df = plot_df.dropna(
        subset=["Goals", "Assists"]
    )

    if plot_df.empty:
        st.info(
            "No valid goals and assists data is available."
        )
        return

    # Create scatter plot
    fig = px.scatter(
        plot_df,
        x="Goals",
        y="Assists",
        hover_name="player_name",
        color="position",
        title="Goals vs Assists: who contributes in both ways?",
        labels={
            "Goals": "Goals scored",
            "Assists": "Assists provided",
        },
    )

    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(
                width=0.7,
                color="white",
            ),
        ),
        hovertemplate=(
            "<b>%{hovertext}</b>"
            "<br>Goals: %{x:.0f}"
            "<br>Assists: %{y:.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=500,
        xaxis_title="Goals Scored",
        yaxis_title="Assists Provided",
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="goals_assists_scatter",
    )

def render_age_performance_scatter(df):
    """
    Display the relationship between player age
    and overall performance index.
    """

    st.markdown(
        """
        <div class="section-kicker">AGE & PERFORMANCE</div>
        <div class="section-title">
            Does age relate to performance?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No player data is available.")
        return

    plot_df = df.copy()

    plot_df["Age"] = pd.to_numeric(
        plot_df["age_2022"],
        errors="coerce",
    )

    plot_df["Performance Index"] = pd.to_numeric(
        plot_df["performance_index"],
        errors="coerce",
    )

    plot_df = plot_df.dropna(
        subset=["Age", "Performance Index"]
    )

    if plot_df.empty:
        st.info(
            "No valid age and performance data is available."
        )
        return

    fig = px.scatter(
        plot_df,
        x="Age",
        y="Performance Index",
        hover_name="player_name",
        color="position",
        title="Age vs Performance Index",
        labels={
            "Age": "Age at World Cup 2022",
            "Performance Index": "Performance Index / 100",
        },
    )

    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(
                width=0.7,
                color="white",
            ),
        ),
        hovertemplate=(
            "<b>%{hovertext}</b>"
            "<br>Age: %{x:.1f}"
            "<br>Performance Index: %{y:.1f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=500,
        xaxis_title="Age at World Cup 2022",
        yaxis_title="Performance Index / 100",
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="age_performance_scatter",
    )

def render_position_performance_boxplot(df):
    """
    Compare performance index distributions across positions.
    """

    st.markdown(
        """
        <div class="section-kicker">POSITION PERFORMANCE</div>
        <div class="section-title">
            How does performance vary by position?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No player data is available.")
        return

    if "position" not in df.columns:
        st.info("Position data is not available.")
        return

    if "performance_index" not in df.columns:
        st.info("Performance index is not available.")
        return

    plot_df = df.copy()

    plot_df["Performance Index"] = pd.to_numeric(
        plot_df["performance_index"],
        errors="coerce",
    )

    plot_df = plot_df.dropna(
        subset=["Performance Index"]
    )

    plot_df["Position"] = plot_df["position"].astype(str)

    if plot_df.empty:
        st.info("No valid performance data is available.")
        return

    fig = px.box(
        plot_df,
        x="Position",
        y="Performance Index",
        color="Position",
        points="all",
        title="Performance Index Distribution by Position",
        labels={
            "Position": "Position",
            "Performance Index": "Performance Index / 100",
        },
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40,
        ),
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="position_performance_boxplot",
    )

def render_top_players_by_position(df):
    """
    Display the highest-performing players within each position.
    """

    st.markdown(
        """
        <div class="section-kicker">POSITION LEADERS</div>
        <div class="section-title">
            Who leads each position?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No player data is available.")
        return

    required_columns = [
        "player_name",
        "position",
        "performance_index",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.info("Required player performance data is not available.")
        return

    plot_df = df.copy()

    plot_df["Performance Index"] = pd.to_numeric(
        plot_df["performance_index"],
        errors="coerce",
    )

    plot_df = plot_df.dropna(
        subset=["Performance Index"]
    )

    plot_df["Position"] = plot_df["position"].astype(str)
    plot_df["Player"] = plot_df["player_name"].astype(str)

    plot_df = plot_df[
        plot_df["Position"].isin(["FW", "MF", "DF", "GK"])
    ]

    if plot_df.empty:
        st.info("No valid position performance data is available.")
        return

    top_players = (
        plot_df
        .sort_values(
            ["Position", "Performance Index"],
            ascending=[True, False],
        )
        .groupby("Position")
        .head(5)
        .copy()
    )

    top_players["Player Position"] = (
        top_players["Player"]
        + " ("
        + top_players["Position"]
        + ")"
    )

    top_players = top_players.sort_values(
        "Performance Index",
        ascending=True,
    )

    fig = px.bar(
        top_players,
        x="Performance Index",
        y="Player Position",
        color="Position",
        orientation="h",
        text="Performance Index",
        title="Top 5 Players by Position",
        labels={
            "Performance Index": "Performance Index / 100",
            "Player Position": "",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
    )

    fig.update_layout(
        height=650,
        margin=dict(
            l=40,
            r=60,
            t=60,
            b=40,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="top_players_by_position",
    )