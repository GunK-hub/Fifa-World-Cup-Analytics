import plotly.express as px
import streamlit as st


def render_overall_rankings(
    ranking_df,
    position_column,
    name_column,
    top_n,
):
    """
    Display the overall Player Performance Index.
    """

    st.markdown(
        '<div class="section-kicker">PLAYER PERFORMANCE INDEX</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            Who is performing across the board?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if ranking_df.empty or not name_column:
        st.info(
            "No players are available for the performance index."
        )
        return

    ranking_columns = [
        name_column,
        "goals_scored",
        "assists_provided",
        "dribbles_per_90",
        "interceptions_per_90",
        "tackles_per_90",
        "total_duels_won_per_90",
        "performance_index",
    ]

    if position_column:
        ranking_columns.insert(1, position_column)

    ranking_display = (
        ranking_df[ranking_columns]
        .sort_values(
            "performance_index",
            ascending=False,
        )
        .head(top_n)
        .copy()
    )

    ranking_display.insert(
        0,
        "Rank",
        range(1, len(ranking_display) + 1),
    )

    rename_columns = {
        name_column: "Player",
        "goals_scored": "Goals",
        "assists_provided": "Assists",
        "dribbles_per_90": "Dribbles / 90",
        "interceptions_per_90": "Interceptions / 90",
        "tackles_per_90": "Tackles / 90",
        "total_duels_won_per_90": "Duels Won / 90",
        "performance_index": "Performance Index",
    }

    if position_column:
        rename_columns[position_column] = "Position"

    ranking_display = ranking_display.rename(
        columns=rename_columns
    )

    left, right = st.columns([1.35, 1])

    with left:

        st.dataframe(
            ranking_display,
            use_container_width=True,
            hide_index=True,
        )

    with right:

        ranking_chart = px.bar(
            ranking_display.sort_values(
                "Performance Index"
            ),
            x="Performance Index",
            y="Player",
            orientation="h",
            title=(
                f"Top {len(ranking_display)} "
                "players by index"
            ),
            labels={
                "Performance Index": "Index / 100",
                "Player": "",
            },
            color_discrete_sequence=["#D6FF52"],
            text="Performance Index",
        )

        ranking_chart.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            hovertemplate=(
                "%{y}<br>"
                "Performance Index: %{x:.1f}"
                "<extra></extra>"
            ),
        )

        ranking_chart.update_layout(
            height=420,
            margin=dict(
                l=10,
                r=20,
                t=60,
                b=20,
            ),
        )

        st.plotly_chart(
            ranking_chart,
            use_container_width=True,
            key="overall_player_performance_index",
        )


def render_position_rankings(
    ranking_df,
    position_column,
    name_column,
    top_n,
):
    """
    Display position-specific player rankings.
    """

    st.markdown(
        """
        <div class="section-kicker">
            POSITION ANALYSIS
        </div>

        <h2 style="margin-top: 0;">
            Who leads each position?
        </h2>

        <p style="color: #9ba393;">
            Compare players using metrics that are
            relevant to their role.
        </p>
        """,
        unsafe_allow_html=True,
    )

    if (
        ranking_df.empty
        or not position_column
        or not name_column
        or "position_index" not in ranking_df.columns
    ):
        st.info(
            "Position ranking data is not available."
        )
        return

    position_options = [
        position
        for position in ["FW", "MF", "DF"]
        if position
        in ranking_df[position_column]
        .dropna()
        .unique()
    ]

    if not position_options:
        st.info(
            "No position data is available."
        )
        return

    selected_position = st.selectbox(
        "Select position",
        position_options,
        key="position_ranking_selector",
    )

    position_df = ranking_df[
        ranking_df[position_column]
        == selected_position
    ].copy()

    position_df["position_index"] = (
        position_df["position_index"]
        .astype(float)
    )

    position_df = (
        position_df
        .sort_values(
            "position_index",
            ascending=False,
        )
        .head(top_n)
        .copy()
    )

    if position_df.empty:
        st.info(
            f"No players found for {selected_position}."
        )
        return

    position_df.insert(
        0,
        "Rank",
        range(1, len(position_df) + 1),
    )

    position_df = position_df.rename(
        columns={
            name_column: "Player",
            position_column: "Position",
            "position_index": "Position Index",
        }
    )

    left, right = st.columns([1.35, 1])

    with left:

        st.dataframe(
            position_df[
                [
                    "Rank",
                    "Player",
                    "Position",
                    "Position Index",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with right:

        chart_df = position_df.sort_values(
            "Position Index",
            ascending=True,
        )

        fig = px.bar(
            chart_df,
            x="Position Index",
            y="Player",
            orientation="h",
            title=(
                f"Top {len(position_df)} "
                f"{selected_position} players"
            ),
            labels={
                "Position Index": "Index / 100",
                "Player": "",
            },
            color_discrete_sequence=["#D6FF52"],
            text="Position Index",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            hovertemplate=(
                "%{y}"
                "<br>Position Index: %{x:.1f}"
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
            key="position_ranking_chart",
        )