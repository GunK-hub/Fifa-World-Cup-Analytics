import html
from pathlib import Path

import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st



from src.position_analysis import calculate_position_index
from src.player_comparison import render_player_comparison
from src.ranking_ui import render_position_rankings
from src.goalkeeper_analysis import (
    calculate_goalkeeper_index,
    render_goalkeeper_analysis,
)
from src.ranking_ui import (
    render_overall_rankings,
    render_position_rankings,
)
from src.player_profile import render_player_profile
from src.advanced_visualizations import (
    render_goals_assists_scatter,
    render_age_performance_scatter,
    render_position_performance_boxplot,
    render_top_players_by_position,
)
from src.nationality_analysis import render_nationality_analysis
from src.correlation_analysis import render_correlation_analysis
from src.statistical_insights import calculate_statistical_insights
from src.player_clustering import (
    calculate_player_clusters,
    render_player_clusters,
)
from src.clustering_evaluation import render_clustering_evaluation

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="World Cup / 22 — Player Atlas",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# App theme
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --pitch: #10130f;
        --panel: #171b16;
        --panel-raised: #1c211b;
        --line: #30372e;
        --ink: #f0f1e8;
        --muted: #9ba393;
        --acid: #d6ff52;
        --coral: #ff795e;
        --sky: #83c8e8;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 78% 2%, rgba(95, 117, 54, 0.16), transparent 34rem),
            linear-gradient(150deg, #10130f 0%, #111510 55%, #0d100d 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(16, 19, 15, 0.72);
    }

    [data-testid="stAppViewContainer"] > .main .block-container {
        max-width: 1480px;
        padding: 2.2rem 3.1rem 3rem;
    }

    [data-testid="stSidebar"] {
        background: #151914;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label {
        color: var(--muted);
    }

    [data-testid="stSidebar"] h2 {
        color: var(--ink);
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.45rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    h1, h2, h3 {
        color: var(--ink);
    }

    h2, h3 {
        font-family: 'Barlow Condensed', Impact, sans-serif;
        font-weight: 700;
        letter-spacing: 0.015em;
    }

    [data-testid="stCaptionContainer"] {
        color: #899281;
    }

    .hero-wrap {
        position: relative;
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 2rem;
        min-height: 258px;
        overflow: hidden;
        padding: 2rem 2.25rem 1.9rem;
        margin: 0.15rem 0 1.8rem;
        border: 1px solid #36402e;
        border-radius: 4px;
        background:
            linear-gradient(106deg, rgba(18, 23, 17, 0.98) 6%, rgba(28, 37, 24, 0.90) 64%, rgba(40, 52, 26, 0.76)),
            repeating-linear-gradient(0deg, transparent 0 31px, rgba(214, 255, 82, 0.035) 32px);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.18);
    }

    .hero-wrap::after {
        content: "";
        position: absolute;
        top: -110px;
        right: 10%;
        width: 360px;
        height: 360px;
        border: 1px solid rgba(214, 255, 82, 0.13);
        border-radius: 50%;
        box-shadow: 0 0 0 30px rgba(214, 255, 82, 0.025), 0 0 0 70px rgba(214, 255, 82, 0.02);
        pointer-events: none;
    }

    .hero-copy, .hero-mark {
        position: relative;
        z-index: 1;
    }

    .hero-eyebrow {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: var(--acid);
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.19em;
        text-transform: uppercase;
    }

    .hero-eyebrow .slash {
        color: #68715f;
    }

    .hero-copy h1 {
        margin: 0.85rem 0 0.35rem;
        color: var(--ink);
        font-family: 'Barlow Condensed', Impact, sans-serif;
        font-size: clamp(3.25rem, 7vw, 6.5rem);
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 0.79;
        text-transform: uppercase;
    }

    .hero-copy h1 span {
        color: var(--acid);
    }

    .hero-copy p {
        margin: 1.1rem 0 0;
        color: #b2baaa;
        font-size: 0.92rem;
    }

    .hero-mark {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        color: #d2d8c8;
        font-size: 0.67rem;
        font-weight: 700;
        letter-spacing: 0.17em;
        line-height: 1.5;
        text-align: right;
        text-transform: uppercase;
    }

    .hero-mark strong {
        color: var(--acid);
        font-family: 'Barlow Condensed', Impact, sans-serif;
        font-size: clamp(4.5rem, 8vw, 7.3rem);
        font-weight: 800;
        letter-spacing: -0.08em;
        line-height: 0.78;
    }

    .dashboard-caption {
        color: var(--muted);
        font-size: 0.92rem;
        margin: -0.45rem 0 1.4rem;
    }

    [data-testid="stMetric"] {
        min-height: 112px;
        background: linear-gradient(145deg, #1b201a 0%, #151914 100%);
        border: 1px solid var(--line);
        border-top: 2px solid var(--acid);
        border-radius: 3px;
        padding: 17px 19px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
        transition: transform 160ms ease, border-color 160ms ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #687b3a;
    }
    [data-testid="stMetricLabel"] {
        color: #a7af9d;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: var(--ink);
        font-family: 'Barlow Condensed', Impact, sans-serif;
        font-size: 2.65rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.05;
    }

    [data-testid="stTabs"] [role="tablist"] {
        gap: 0.35rem;
        border-bottom: 1px solid var(--line);
    }
    [data-testid="stTabs"] button[role="tab"] {
        min-height: 2.8rem;
        padding: 0 1rem;
        color: #9ba393;
        border: 0;
        border-bottom: 2px solid transparent;
        background: transparent;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.045em;
        text-transform: uppercase;
    }
    [data-testid="stTabs"] button[role="tab"]:hover {
        color: var(--ink);
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--acid);
        border-bottom-color: var(--acid);
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: var(--acid);
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
    [data-testid="stTextInput"] input {
        color: var(--ink);
        background: #1b201a;
        border-color: #394035;
        border-radius: 3px;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--acid);
    }
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background-color: var(--acid);
    }

    [data-testid="stPlotlyChart"] {
        margin: 0.25rem 0 0.8rem;
        padding: 0.3rem 0.6rem 0.1rem;
        border: 1px solid #293027;
        border-radius: 3px;
        background: rgba(23, 27, 22, 0.72);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 3px;
    }

    .section-kicker {
        margin: 1.1rem 0 0.5rem;
        color: var(--acid);
        font-family: 'Barlow Condensed', Impact, sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .section-note {
        color: #7f8978;
        font-size: 0.76rem;
        letter-spacing: 0.025em;
    }

    [data-testid="stDownloadButton"] button {
        color: #151914;
        border: 1px solid var(--acid);
        border-radius: 2px;
        background: var(--acid);
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    [data-testid="stDownloadButton"] button:hover {
        color: #151914;
        border-color: #e4ff91;
        background: #e4ff91;
    }

    [data-testid="stAlert"] {
        border-radius: 3px;
    }

    @media (max-width: 760px) {
        [data-testid="stAppViewContainer"] > .main .block-container {
            padding: 1.2rem 1rem 2rem;
        }
        .hero-wrap {
            min-height: 225px;
            padding: 1.5rem 1.2rem;
        }
        .hero-mark {
            display: none;
        }
        .hero-copy h1 {
            font-size: clamp(3rem, 16vw, 5rem);
        }
        [data-testid="stTabs"] button[role="tab"] {
            padding: 0 0.55rem;
            font-size: 0.68rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Load and prepare dataset
# -----------------------------
DATA_PATH = Path("data/Processed/players_clean.csv")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)

    # Make text columns consistent and numeric columns safe for aggregation.
    for column in ["player_name", "name", "nationality", "position", "team"]:
        if column in data.columns:
            data[column] = data[column].fillna("Unknown").astype(str).str.strip()

    for column in [
        "goals_scored",
        "assists_provided",
        "appearances",
        "minutes_played",
        "shots",
        "shots_on_target",
        "passes_completed",
    ]:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)

    if "player_dob" in data.columns:
        data["player_dob"] = pd.to_datetime(data["player_dob"], errors="coerce")
        # FIFA 2022 ended on 18 December 2022; use exact days rather than
        # subtracting only birth years.
        data["age_2022"] = (
            (pd.Timestamp("2022-12-18") - data["player_dob"]).dt.days / 365.25
        )

    return data


try:
    df = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(
        f"Could not find `{DATA_PATH}`. Place players_clean.csv in "
        "`data/Processed/` and refresh the app."
    )
    st.stop()
except Exception as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()


def first_existing(columns: list[str], frame: pd.DataFrame) -> str | None:
    """Return the first column that exists in frame."""
    return next((column for column in columns if column in frame.columns), None)


def number_column(frame: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric series even when a source column is missing."""
    if column not in frame.columns:
        return pd.Series(0, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").fillna(0)


def format_number(value: float, decimals: int = 0) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}"


def player_label(frame: pd.DataFrame) -> str:
    return first_existing(["player_name", "name", "player"], frame) or "Player"


def chart_layout(fig, height: int = 390):
    """Apply a consistent, presentation-friendly Plotly layout."""
    fig.update_layout(
        height=height,
        margin=dict(l=16, r=16, t=58, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#dfe4d6", size=12),
        title_font=dict(family="Barlow Condensed, sans-serif", size=20, color="#f0f1e8"),
        legend_title_text="",
        hoverlabel=dict(bgcolor="#20261e", bordercolor="#59624f", font_color="#f0f1e8", font_size=12),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color="#a7af9d"))
    fig.update_yaxes(gridcolor="rgba(173,184,160,0.12)", zeroline=False, tickfont=dict(color="#a7af9d"))
    return fig


# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Match filters")
st.sidebar.caption("Refine the player index. Every view updates with your selection.")

nationality_column = first_existing(["nationality", "country"], df)
position_column = first_existing(["position", "player_position"], df)

if nationality_column:
    nationality_options = sorted(
        df[nationality_column].dropna().astype(str).unique().tolist()
    )
    selected_nationalities = st.sidebar.multiselect(
        "Nationality",
        nationality_options,
        placeholder="All nationalities",
    )
else:
    selected_nationalities = []

if position_column:
    position_options = sorted(
        df[position_column].dropna().astype(str).unique().tolist()
    )
    selected_positions = st.sidebar.multiselect(
        "Position",
        position_options,
        placeholder="All positions",
    )
else:
    selected_positions = []

name_column = first_existing(["player_name", "name", "player"], df)
search_text = ""
if name_column:
    search_text = st.sidebar.text_input(
        "Search player",
        placeholder="e.g. Mbappé",
    ).strip().lower()

if "age_2022" in df.columns and df["age_2022"].notna().any():
    min_age = int(df["age_2022"].dropna().min())
    max_age = int(df["age_2022"].dropna().max())
    if min_age < max_age:
        selected_age = st.sidebar.slider(
            "Age at World Cup 2022",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
        )
    else:
        selected_age = (min_age, max_age)
else:
    selected_age = None

top_n = st.sidebar.slider("Show top performers", 5, 20, 10)


# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df.copy()

if nationality_column and selected_nationalities:
    filtered_df = filtered_df[
        filtered_df[nationality_column].isin(selected_nationalities)
    ]

if position_column and selected_positions:
    filtered_df = filtered_df[filtered_df[position_column].isin(selected_positions)]

if name_column and search_text:
    filtered_df = filtered_df[
        filtered_df[name_column].astype(str).str.lower().str.contains(
            search_text, na=False
        )
    ]

if selected_age and "age_2022" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["age_2022"].between(selected_age[0], selected_age[1])
    ]


# -----------------------------
# Player Performance Index
# -----------------------------
def min_max_normalize(series):
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(0, index=series.index, dtype="float64")

    return (series - min_value) / (max_value - min_value)


performance_metrics = {
    "goals_scored": "Goals",
    "assists_provided": "Assists",
    "dribbles_per_90": "Dribbles / 90",
    "interceptions_per_90": "Interceptions / 90",
    "tackles_per_90": "Tackles / 90",
    "total_duels_won_per_90": "Duels Won / 90",
}

ranking_df = filtered_df.copy()

for column in performance_metrics:
    ranking_df[column] = number_column(
        ranking_df,
        column,
    )

# Normalize using the FULL dataset
# so the index stays consistent when filters change.

normalized_columns = []

for column in performance_metrics:
    normalized_column = f"{column}_normalized"

    full_series = number_column(df, column)

    min_value = full_series.min()
    max_value = full_series.max()

    if max_value == min_value:
        ranking_df[normalized_column] = 0.0
    else:
        ranking_df[normalized_column] = (
            ranking_df[column] - min_value
        ) / (max_value - min_value)

    normalized_columns.append(normalized_column)


# Equal-weight performance index
ranking_df["performance_index"] = (
    ranking_df[normalized_columns]
    .mean(axis=1)
    * 100
)

ranking_df["performance_index"] = (
    ranking_df["performance_index"].round(1)
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero-wrap">
      <div class="hero-copy">
        <div class="hero-eyebrow">Qatar 2022 <span class="slash">/</span> Player index</div>
        <h1>The game,<br><span>in numbers.</span></h1>
        <p>Every finish, chance and player profile from football’s biggest stage.</p>
      </div>
      <div class="hero-mark">
        <span>FIFA World Cup</span>
        <strong>22</strong>
        <span>Player atlas</span>
      </div>
    </div>
    <p class="dashboard-caption">A closer look at the people and performances behind Qatar 2022.</p>
    """,
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.warning("No players match the current filters. Try widening your selection.")
    st.stop()


# -----------------------------
# Filter-aware KPI cards
# -----------------------------
goals = number_column(filtered_df, "goals_scored").sum()
assists = number_column(filtered_df, "assists_provided").sum()
average_age = filtered_df["age_2022"].mean() if "age_2022" in filtered_df else None

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Players in view", format_number(len(filtered_df)))
kpi_2.metric("Goals scored", format_number(goals))
kpi_3.metric("Assists provided", format_number(assists))
kpi_4.metric(
    "Average age",
    f"{average_age:.1f}" if pd.notna(average_age) else "—",
)

st.caption(
    f"PLAYER INDEX  /  {len(filtered_df):,} OF {len(df):,} PLAYERS IN VIEW  /  "
    f"{len(filtered_df) / len(df):.0%} OF DATASET"
)


# -----------------------------
# Dashboard tabs
# -----------------------------
overview_tab, performance_tab, comparison_tab, nationality_tab, table_tab = st.tabs(
    [
        "Overview",
        "Player performance",
        "Head to head",
        "Nationalities",
        "Data explorer",
    ]
)



            # -----------------------------
# Team & nationality analysis
# -----------------------------
with nationality_tab:
    st.subheader("Nationalities & squads")
    st.caption(
        "Explore player representation and attacking contribution across nationalities."
    )

    if nationality_column:
        nationality_df = filtered_df.copy()

        nationality_df["Goals"] = number_column(
            nationality_df,
            "goals_scored",
        )

        nationality_df["Assists"] = number_column(
            nationality_df,
            "assists_provided",
        )

        # -----------------------------
        # Nationality KPIs
        # -----------------------------
        total_nationalities = nationality_df[nationality_column].nunique()

        top_nationality = (
            nationality_df.groupby(nationality_column)["Goals"]
            .sum()
            .sort_values(ascending=False)
        )

        top_nationality_name = (
            top_nationality.index[0]
            if len(top_nationality) > 0
            else "—"
        )

        top_nationality_goals = (
            top_nationality.iloc[0]
            if len(top_nationality) > 0
            else 0
        )

        kpi_1, kpi_2, kpi_3 = st.columns(3)

        kpi_1.metric(
            "Nationalities",
            format_number(total_nationalities),
        )

        kpi_2.metric(
            "Top nationality by goals",
            top_nationality_name,
        )

        kpi_3.metric(
            "Goals from top nationality",
            format_number(top_nationality_goals),
        )

        st.divider()

        # -----------------------------
        # Goals & assists by nationality
        # -----------------------------
        left, right = st.columns(2)

        with left:
            nationality_goals = (
                nationality_df.groupby(
                    nationality_column,
                    as_index=False,
                )["Goals"]
                .sum()
                .sort_values("Goals", ascending=False)
                .head(top_n)
                .sort_values("Goals")
            )

            fig = px.bar(
                nationality_goals,
                x="Goals",
                y=nationality_column,
                orientation="h",
                title=f"Top {min(top_n, len(nationality_goals))} nationalities by goals",
                labels={
                    nationality_column: "",
                    "Goals": "Goals scored",
                },
                color_discrete_sequence=["#D6FF52"],
                text="Goals",
            )

            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                hovertemplate=(
                    "%{y}<br>"
                    "Goals: %{x:.0f}"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                chart_layout(fig),
                use_container_width=True,
            )

        with right:
            nationality_assists = (
                nationality_df.groupby(
                    nationality_column,
                    as_index=False,
                )["Assists"]
                .sum()
                .sort_values("Assists", ascending=False)
                .head(top_n)
                .sort_values("Assists")
            )

            fig = px.bar(
                nationality_assists,
                x="Assists",
                y=nationality_column,
                orientation="h",
                title=f"Top {min(top_n, len(nationality_assists))} nationalities by assists",
                labels={
                    nationality_column: "",
                    "Assists": "Assists provided",
                },
                color_discrete_sequence=["#FF795E"],
                text="Assists",
            )

            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                hovertemplate=(
                    "%{y}<br>"
                    "Assists: %{x:.0f}"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                chart_layout(fig),
                use_container_width=True,
            )

        # -----------------------------
        # Player distribution
        # -----------------------------
        st.markdown('<div class="section-kicker">Squad representation</div>', unsafe_allow_html=True)

        player_distribution = (
            nationality_df.groupby(
                nationality_column,
                as_index=False,
            )
            .size()
            .rename(columns={"size": "Players"})
            .sort_values("Players", ascending=False)
            .head(top_n)
            .sort_values("Players")
        )

        fig = px.bar(
            player_distribution,
            x="Players",
            y=nationality_column,
            orientation="h",
            title=f"Top {min(top_n, len(player_distribution))} nationalities by player count",
            labels={
                nationality_column: "",
                "Players": "Number of players",
            },
            color_discrete_sequence=["#83C8E8"],
            text="Players",
        )

        fig.update_traces(
            texttemplate="%{text:.0f}",
            textposition="outside",
            hovertemplate=(
                "%{y}<br>"
                "Players: %{x:.0f}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig, height=430),
            use_container_width=True,
        )

    else:
        st.info(
            "A nationality column was not found in the dataset."
        )

with overview_tab:
    left, right = st.columns(2)

    with left:
        if nationality_column:
            nationality_summary = (
                filtered_df.assign(
                    Goals=number_column(filtered_df, "goals_scored"),
                    Assists=number_column(filtered_df, "assists_provided"),
                )
                .groupby(nationality_column, as_index=False)[["Goals", "Assists"]]
                .sum()
                .sort_values("Goals", ascending=False)
                .head(top_n)
            )

            fig = px.bar(
                nationality_summary.sort_values("Goals"),
                x="Goals",
                y=nationality_column,
                orientation="h",
                title=f"Top {min(top_n, len(nationality_summary))} nationalities by goals",
                labels={nationality_column: "", "Goals": "Goals scored"},
                color_discrete_sequence=["#D6FF52"],
                text="Goals",
            )
            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                hovertemplate="%{y}<br>Goals: %{x:.0f}<extra></extra>",
            )
            st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
            key="overview_nationality_goals"
        )
        else:
            st.info("A nationality column was not found in the dataset.")

    with right:
        if position_column:
            position_summary = (
                filtered_df.assign(
                    Goals=number_column(filtered_df, "goals_scored"),
                    Assists=number_column(filtered_df, "assists_provided"),
                )
                .groupby(position_column, as_index=False)[["Goals", "Assists"]]
                .sum()
                .sort_values("Goals", ascending=False)
            )

            fig = px.bar(
                position_summary,
                x=position_column,
                y=["Goals", "Assists"],
                barmode="group",
                title="Attacking output by position",
                labels={
                    position_column: "",
                    "value": "Contributions",
                    "variable": "",
                },
                color_discrete_sequence=["#D6FF52", "#FF795E"],
            )
            fig.update_traces(
                hovertemplate="%{x}<br>%{fullData.name}: %{y:.0f}<extra></extra>"
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)
        else:
            st.info("A position column was not found in the dataset.")

    if "age_2022" in filtered_df.columns:
        fig = px.histogram(
            filtered_df.dropna(subset=["age_2022"]),
            x="age_2022",
            nbins=14,
            title="Age distribution of players in view",
            labels={"age_2022": "Age at World Cup 2022", "count": "Players"},
                color_discrete_sequence=["#83C8E8"],
        )
        fig.update_traces(
            hovertemplate="Age: %{x:.0f}<br>Players: %{y}<extra></extra>"
        )
        st.plotly_chart(chart_layout(fig, height=350), use_container_width=True)

         # -------------------------
    # PLAYER PERFORMANCE INDEX
    # -------------------------

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

    if not ranking_df.empty and name_column:

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
            .sort_values("performance_index", ascending=False)
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
                title=f"Top {len(ranking_display)} players by index",
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

            st.plotly_chart(
                chart_layout(ranking_chart),
                use_container_width=True,
                key="overview_player_performance_index",
            )

    else:

        st.info(
            "No players are available for the performance index."
        )

with performance_tab:

    render_overall_rankings(
        ranking_df,
        position_column,
        name_column,
        top_n,
    )

    position_ranking_df = calculate_position_index(
        ranking_df,
        position_column=position_column,
    )

    clustered_df = calculate_player_clusters(
    ranking_df,
    name_column,
    )

    statistical_insights = calculate_statistical_insights(
    ranking_df,
    name_column=name_column,
    position_column=position_column,
    nationality_column=nationality_column,
    )


    goalkeeper_ranking_df = calculate_goalkeeper_index(
    ranking_df,
    position_column=position_column,
    )  

    render_position_rankings(
    position_ranking_df,
    position_column,
    name_column,
    top_n,
    )

    render_goalkeeper_analysis(
    goalkeeper_ranking_df,
    name_column,
    position_column,
    top_n,
    )

    render_player_profile(
    ranking_df,
    name_column,
    position_column,
    )

    st.divider()

    st.divider()

    performance_df = filtered_df.copy()
    performance_df["Goals"] = number_column(
        performance_df,
        "goals_scored",
    )
    performance_df["Assists"] = number_column(
        performance_df,
        "assists_provided",
    )

    left, right = st.columns(2)

    with left:
        if name_column:
            top_goals = (
                performance_df.groupby(name_column, as_index=False)["Goals"]
                .sum()
                .sort_values("Goals", ascending=False)
                .head(top_n)
                .sort_values("Goals")
            )
            fig = px.bar(
                top_goals,
                x="Goals",
                y=name_column,
                orientation="h",
                title=f"Top {min(top_n, len(top_goals))} goal scorers",
                labels={name_column: "", "Goals": "Goals scored"},
                color_discrete_sequence=["#D6FF52"],
                text="Goals",
            )
            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                hovertemplate="%{y}<br>Goals: %{x:.0f}<extra></extra>",
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)
        else:
            st.info("A player-name column was not found in the dataset.")

    with right:
        if name_column:
            top_assists = (
                performance_df.groupby(name_column, as_index=False)["Assists"]
                .sum()
                .sort_values("Assists", ascending=False)
                .head(top_n)
                .sort_values("Assists")
            )
            fig = px.bar(
                top_assists,
                x="Assists",
                y=name_column,
                orientation="h",
                title=f"Top {min(top_n, len(top_assists))} assist providers",
                labels={name_column: "", "Assists": "Assists provided"},
                color_discrete_sequence=["#FF795E"],
                text="Assists",
            )
            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                hovertemplate="%{y}<br>Assists: %{x:.0f}<extra></extra>",
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)
        else:
            st.info("A player-name column was not found in the dataset.")

        render_goals_assists_scatter(
        filtered_df,
       )
        render_age_performance_scatter(
        ranking_df,
       )
        render_position_performance_boxplot(
        ranking_df,
       )
        render_top_players_by_position(
         ranking_df,
       )
        render_nationality_analysis(
        ranking_df,
        nationality_column,
        name_column,
        top_n,
       )

        render_correlation_analysis(
        ranking_df,
        )

        render_player_clusters(
            clustered_df,
            name_column,
            position_column,
        )
        render_clustering_evaluation(
        ranking_df,
        clustered_df,
        )

        st.markdown(
        '<div class="section-kicker">STATISTICAL INSIGHTS</div>',
        unsafe_allow_html=True,
       )

        st.markdown(
            """
            <div class="section-title">
                What does the data tell us?
            </div>
            """,
            unsafe_allow_html=True,
        )

        if statistical_insights:
            for insight_name, insight_data in statistical_insights.items():

                st.markdown(
                    f"### {insight_name.replace('_', ' ').title()}"
                )

                if hasattr(insight_data, "style"):
                    st.dataframe(
                        insight_data,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.write(insight_data)

        with comparison_tab:
            render_player_comparison(
            ranking_df,
            name_column,
            position_column,
        )


with table_tab:
    st.subheader("Filtered player data")
    st.caption("Use the column headers to sort. Download the filtered view for your report.")

    display_df = filtered_df.copy()
    if "age_2022" in display_df.columns:
        display_df["age_2022"] = display_df["age_2022"].round(1)
    if "player_dob" in display_df.columns:
        display_df["player_dob"] = display_df["player_dob"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=520,
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv_data,
        file_name="fifa_2022_filtered_players.csv",
        mime="text/csv",
    )


# -----------------------------
# Footer
# -----------------------------
st.divider()
st.markdown(
    '<p class="section-note">Source: FIFA World Cup 2022 player dataset · '
    "Calculated age uses 18 December 2022 as the reference date.</p>",
    unsafe_allow_html=True,
)