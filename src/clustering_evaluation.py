import pandas as pd
import plotly.express as px
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


CLUSTER_METRICS = [
    "goals_scored",
    "assists_provided",
    "dribbles_per_90",
    "interceptions_per_90",
    "tackles_per_90",
    "total_duels_won_per_90",
]


def prepare_cluster_data(df):
    """
    Prepare numerical player metrics for clustering evaluation.
    """

    available_metrics = [
        metric
        for metric in CLUSTER_METRICS
        if metric in df.columns
    ]

    if len(available_metrics) < 2:
        return None, []

    model_data = df[available_metrics].copy()

    for metric in available_metrics:
        model_data[metric] = pd.to_numeric(
            model_data[metric],
            errors="coerce",
        )

    model_data = model_data.fillna(0)

    return model_data, available_metrics


def calculate_silhouette_scores(df):
    """
    Calculate silhouette scores for different numbers of clusters.
    """

    model_data, available_metrics = prepare_cluster_data(df)

    if model_data is None or len(model_data) < 3:
        return pd.DataFrame()

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(model_data)

    max_clusters = min(8, len(model_data) - 1)

    scores = []

    for n_clusters in range(2, max_clusters + 1):

        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
        )

        labels = kmeans.fit_predict(scaled_data)

        score = silhouette_score(
            scaled_data,
            labels,
        )

        scores.append(
            {
                "Clusters": n_clusters,
                "Silhouette Score": round(score, 3),
            }
        )

    return pd.DataFrame(scores)

def render_clustering_evaluation(
    df,
    clustered_df=None,
):
    """
    Display clustering evaluation and PCA visualization.
    """

    st.markdown(
        '<div class="section-kicker">CLUSTERING EVALUATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            How meaningful are the player groups?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info(
            "No player data is available for clustering evaluation."
        )
        return

    # --------------------------------
    # Silhouette Score
    # --------------------------------

    scores_df = calculate_silhouette_scores(df)

    if scores_df.empty:
        st.info(
            "Not enough data is available to evaluate clustering."
        )
        return

    best_row = scores_df.loc[
        scores_df["Silhouette Score"].idxmax()
    ]

    # --------------------------------
    # Silhouette Score Chart
    # --------------------------------

    fig = px.line(
        scores_df,
        x="Clusters",
        y="Silhouette Score",
        markers=True,
        title="Choosing the number of clusters",
        labels={
            "Clusters": "Number of Clusters",
            "Silhouette Score": "Silhouette Score",
        },
    )

    fig.update_layout(
        height=420,
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
        key="clustering_silhouette_scores",
    )

    # --------------------------------
    # Clustering Metrics
    # --------------------------------

    metric_1, metric_2 = st.columns(2)

    with metric_1:
        st.metric(
            "Highest Silhouette Score",
            f"{best_row['Silhouette Score']:.3f}",
        )

    with metric_2:
        st.metric(
            "Cluster Count",
            int(best_row["Clusters"]),
        )

    st.caption(
        "Higher silhouette scores generally indicate "
        "better-separated clusters."
    )

    # --------------------------------
    # PCA Visualization
    # --------------------------------

    if (
        clustered_df is None
        or "cluster" not in clustered_df.columns
    ):
        return

    model_data, available_metrics = prepare_cluster_data(
        clustered_df
    )

    if model_data is None or len(model_data) < 3:
        return

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(model_data)

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    pca_data = pca.fit_transform(scaled_data)

    pca_df = pd.DataFrame(
        {
            "PC1": pca_data[:, 0],
            "PC2": pca_data[:, 1],
            "Cluster": clustered_df["cluster"].astype(str).values,
        }
    )

    if "player_name" in clustered_df.columns:
        pca_df["Player"] = (
            clustered_df["player_name"]
            .fillna("Unknown")
            .astype(str)
        )

    st.markdown(
        """
        <div class="section-title">
            Player clusters in 2D
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="Cluster",
        hover_name=(
            "Player"
            if "Player" in pca_df.columns
            else None
        ),
        title="PCA projection of player profiles",
    )

    fig.update_layout(
        height=550,
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
        key="player_cluster_pca",
    )

    explained_variance = (
        pca.explained_variance_ratio_.sum() * 100
    )

    st.caption(
        f"The two PCA dimensions explain "
        f"{explained_variance:.1f}% of the variance "
        f"in the selected performance metrics."
  )