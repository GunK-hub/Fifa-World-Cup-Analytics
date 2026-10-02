import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import streamlit as st

CLUSTER_METRICS = [
    "goals_scored",
    "assists_provided",
    "dribbles_per_90",
    "interceptions_per_90",
    "tackles_per_90",
    "total_duels_won_per_90",
]


def calculate_player_clusters(
    df,
    name_column,
    n_clusters=5,
):
    """
    Group players into statistical clusters
    using K-Means clustering.
    """

    result = df.copy()

    available_metrics = [
        metric
        for metric in CLUSTER_METRICS
        if metric in result.columns
    ]

    if len(available_metrics) < 2:
        return result

    model_data = result[available_metrics].copy()

    for metric in available_metrics:
        model_data[metric] = pd.to_numeric(
            model_data[metric],
            errors="coerce",
        )

    model_data = model_data.fillna(0)

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        model_data
    )

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
    )

    result["cluster"] = kmeans.fit_predict(
        scaled_data
    )

    return result

def render_player_clusters(
    clustered_df,
    name_column,
    position_column,
):
    """
    Display player clusters based on performance metrics.
    """

    st.markdown(
        """
        <div class="section-kicker">
            PLAYER CLUSTERING
        </div>

        <div class="section-title">
            Which players have similar profiles?
        </div>

        <p style="color: #9ba393;">
            Group players with similar performance characteristics.
        </p>
        """,
        unsafe_allow_html=True,
    )

    if clustered_df.empty or "cluster" not in clustered_df.columns:
        st.info("Player clustering data is not available.")
        return

    cluster_df = clustered_df.copy()

    cluster_df["cluster"] = (
        pd.to_numeric(
            cluster_df["cluster"],
            errors="coerce",
        )
        .astype("Int64")
    )

    cluster_options = sorted(
        cluster_df["cluster"]
        .dropna()
        .unique()
        .tolist()
    )

    if not cluster_options:
        st.info("No player clusters are available.")
        return

    selected_cluster = st.selectbox(
        "Select player group",
        cluster_options,
        key="player_cluster_selector",
    )

    selected_df = cluster_df[
        cluster_df["cluster"] == selected_cluster
    ].copy()

    if selected_df.empty:
        st.info("No players found in this cluster.")
        return

    display_columns = []

    if name_column:
        display_columns.append(name_column)

    if position_column:
        display_columns.append(position_column)

    display_columns += [
        "goals_scored",
        "assists_provided",
        "dribbles_per_90",
        "tackles_per_90",
        "total_duels_won_per_90",
        "cluster",
    ]

    display_columns = [
        column
        for column in display_columns
        if column in selected_df.columns
    ]

    st.dataframe(
        selected_df[display_columns],
        use_container_width=True,
        hide_index=True,
    )