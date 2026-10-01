import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_player_profile(
    df,
    name_column,
    position_column,
):
    """
    Display a detailed profile for a selected player.
    """

    st.markdown(
        """
        <div class="section-kicker">PLAYER DEEP DIVE</div>
        <div class="section-title">
            Explore an individual player's performance
        </div>
        """,
        unsafe_allow_html=True,
    )
    if df.empty or not name_column:
        st.info("Player profile data is not available.")
        return

    player_options = sorted(
        df[name_column]
        .dropna()
        .astype(str)
        .unique()
    )

    if not player_options:
        st.info("No players are available.")
        return

    selected_player = st.selectbox(
        "Select player",
        player_options,
        key="player_profile_selector",
    )

    player_data = df[
        df[name_column].astype(str) == selected_player
    ].iloc[0]

    player_position = (
        player_data[position_column]
        if position_column
        else "N/A"
    )
    player_nationality = player_data.get(
    "nationality",
    "N/A",
    )

    player_club = player_data.get(
    "club",
    "N/A",
    )

    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-name">
                {selected_player}
            </div>
            <div class="profile-position">
                {player_position} · {player_nationality} · {player_club}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    goals = pd.to_numeric(
        player_data.get("goals_scored", 0),
        errors="coerce",
    )

    assists = pd.to_numeric(
        player_data.get("assists_provided", 0),
        errors="coerce",
    )

    dribbles = pd.to_numeric(
        player_data.get("dribbles_per_90", 0),
        errors="coerce",
    )

    tackles = pd.to_numeric(
        player_data.get("tackles_per_90", 0),
        errors="coerce",
    )

    interceptions = pd.to_numeric(
        player_data.get("interceptions_per_90", 0),
        errors="coerce",
    )

    duels = pd.to_numeric(
        player_data.get("total_duels_won_per_90", 0),
        errors="coerce",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Goals", goals)

    with col2:
        st.metric("Assists", assists)

    with col3:
        st.metric("Dribbles / 90", dribbles)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Tackles / 90", tackles)

    with col5:
        st.metric("Interceptions / 90", interceptions)

    with col6:
        st.metric("Duels Won / 90", duels)

        performance_index = pd.to_numeric(
        player_data.get("performance_index", 0),
        errors="coerce",
    )

    if pd.isna(performance_index):
        performance_index = 0

        st.metric(
        "Performance Index",
        round(float(performance_index), 1),
    )

    chart_labels = [
        "Goals",
        "Assists",
        "Dribbles / 90",
        "Tackles / 90",
        "Interceptions / 90",
        "Duels Won / 90",
    ]

    chart_values = [
        float(goals),
        float(assists),
        float(dribbles),
        float(tackles),
        float(interceptions),
        float(duels),
    ]

    fig = go.Figure(
        go.Bar(
            x=chart_values,
            y=chart_labels,
            orientation="h",
        )
    )

    fig.update_layout(
        title=f"{selected_player} — Performance Breakdown",
        xaxis_title="Value",
        yaxis_title="Metric",
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="player_profile_performance_breakdown",
    )    