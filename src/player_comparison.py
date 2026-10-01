import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_player_comparison(
    ranking_df,
    name_column,
    position_column,
):
    """
    Display a side-by-side comparison of two players.
    """

    st.markdown(
        """
        <div class="section-kicker">PLAYER COMPARISON</div>
        <div class="section-title">
            How do two players compare?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if ranking_df.empty or not name_column:
        st.info("Player comparison data is not available.")
        return

    comparison_df = ranking_df.copy()

    comparison_df[name_column] = (
        comparison_df[name_column]
        .fillna("Unknown")
        .astype(str)
    )

    player_options = sorted(
        comparison_df[name_column].unique()
    )

    if len(player_options) < 2:
        st.info("At least two players are required for comparison.")
        return

    left_select, right_select = st.columns(2)

    with left_select:
        player_1 = st.selectbox(
            "Player 1",
            player_options,
            index=0,
            key="comparison_player_1",
        )

    with right_select:
        player_2 = st.selectbox(
            "Player 2",
            player_options,
            index=1,
            key="comparison_player_2",
        )

    player_1_data = comparison_df[
        comparison_df[name_column] == player_1
    ].iloc[0]

    player_2_data = comparison_df[
        comparison_df[name_column] == player_2
    ].iloc[0]

    metrics = {
        "Goals": "goals_scored",
        "Assists": "assists_provided",
        "Dribbles / 90": "dribbles_per_90",
        "Interceptions / 90": "interceptions_per_90",
        "Tackles / 90": "tackles_per_90",
        "Duels Won / 90": "total_duels_won_per_90",
    }

    comparison_rows = []

    for label, column in metrics.items():

        value_1 = pd.to_numeric(
            player_1_data.get(column, 0),
            errors="coerce",
        )

        value_2 = pd.to_numeric(
            player_2_data.get(column, 0),
            errors="coerce",
        )

        if pd.isna(value_1):
            value_1 = 0

        if pd.isna(value_2):
            value_2 = 0

        comparison_rows.append(
            {
                "Metric": label,
                player_1: round(float(value_1), 2),
                player_2: round(float(value_2), 2),
            }
        )

    comparison_table = pd.DataFrame(comparison_rows)

    st.dataframe(
        comparison_table,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------
    # Radar chart
    # --------------------------------

    labels = list(metrics.keys())

    values_1 = comparison_table[player_1].tolist()
    values_2 = comparison_table[player_2].tolist()

    # Normalize the two players against each other
    normalized_1 = []
    normalized_2 = []

    for value_1, value_2 in zip(values_1, values_2):

        maximum = max(value_1, value_2)

        if maximum == 0:
            normalized_1.append(0)
            normalized_2.append(0)
        else:
            normalized_1.append(value_1 / maximum)
            normalized_2.append(value_2 / maximum)

    radar = go.Figure()

    radar.add_trace(
        go.Scatterpolar(
            r=normalized_1 + [normalized_1[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=player_1,
        )
    )

    radar.add_trace(
        go.Scatterpolar(
            r=normalized_2 + [normalized_2[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=player_2,
        )
    )

    radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
            )
        ),
        height=500,
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40,
        ),
        title="Player Performance Comparison",
    )

    st.plotly_chart(
        radar,
        use_container_width=True,
        key="player_comparison_radar",
    )