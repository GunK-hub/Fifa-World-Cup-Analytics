# FIFA World Cup 2022 Player Analytics

An interactive Streamlit dashboard for exploring player statistics from the 2022 FIFA World Cup. Filter players by nationality, position, name, and age, then compare performance, explore team-level summaries, and download the filtered data.

## Features

- **Overview:** player, goal, assist, and age KPIs; nationality and position summaries; player performance rankings.
- **Player performance:** attacking and defensive visualizations, position-specific rankings, goalkeeper analysis, player profiles, correlation analysis, clustering, and statistical insights.
- **Head to head:** compare player performance.
- **Nationalities:** explore squad representation and attacking contributions by nationality.
- **Data explorer:** inspect the filtered player records and download them as a CSV.
- **Sidebar filters:** narrow the dashboard by nationality, position, player name, age at the 2022 World Cup, and number of top performers to show.

## Project structure

```text
.
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   │   └── FIFA WC 2022 Players Stats.csv
│   └── Processed/
│       └── players_clean.csv
├── notebooks/
│   ├── 01_data_loading.ipynb
│   └── 02_eda.ipynb
├── src/                 # Dashboard analysis and visualization modules
└── requirements.txt
```

## Run the dashboard

Run these commands from the project root directory. The dashboard loads `data/Processed/players_clean.csv` using a path relative to the current working directory.

### 1. Create and activate a virtual environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies and launch Streamlit

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Streamlit will print a local URL in the terminal; open it in a browser to use the dashboard.

## Data and notebooks

The repository includes the raw World Cup player statistics CSV and a cleaned CSV used by the dashboard. The notebooks contain data preparation and exploratory analysis.

To run the notebooks, install Jupyter and the additional plotting libraries used there:

```bash
pip install jupyter matplotlib seaborn
jupyter notebook
```

**Notebook path note:** the notebooks refer to `data/processed/players_clean.csv` (lowercase `processed`), while the included directory is named `data/Processed/`. On case-sensitive systems, update the notebook paths to match the actual directory before running them.

## Dependencies

The dashboard dependencies are pinned in `requirements.txt`: pandas, NumPy, Plotly, scikit-learn, and Streamlit.

## Data attribution

The included files do not specify the dataset's source or license. Add the original source and licensing details here before redistributing the dataset.
