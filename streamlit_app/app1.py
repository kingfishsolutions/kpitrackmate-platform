import os
import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(
    page_title="NextGen KPI Sports Performance",
    page_icon="🏆",
    layout="wide",
)


@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


@st.cache_data(ttl=60)
def run_query(query, params=None):
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)


st.title("NextGen KPI Sports Performance")
st.caption("Junior teams get better, faster — Live Player & Team KPI Analytics")

# Verify database tables exist
try:
    kpi_df = run_query(
        """
        SELECT
            pmk.performance_id,
            s.season_name,
            l.abbreviation AS league,
            t.name AS team_name,
            a.athlete_id,
            CONCAT(
                CASE WHEN a.jersey_number IS NOT NULL THEN '#' || a.jersey_number || ' ' ELSE '' END,
                a.first_name, ' ', a.last_name
            ) AS athlete_name,
            a.position,
            kc.category_name AS kpi_category,
            k.kpi_name,
            pmk.actual_value,
            COALESCE(pmk.target_value, k.target_value) AS target_value,
            m.match_id,
            ht.name || ' vs ' || at.name AS match_label,
            pmk.recorded_at
        FROM player_match_kpis pmk
        JOIN athlete a ON pmk.player_id = a.athlete_id
        LEFT JOIN team t ON a.team_id = t.team_id
        JOIN kpi k ON pmk.kpi_id = k.kpi_id
        JOIN kpi_category kc ON k.category_id = kc.category_id
        JOIN match m ON pmk.match_id = m.match_id
        JOIN season s ON m.season_id = s.season_id
        JOIN league l ON s.league_id = l.league_id
        JOIN team ht ON m.home_team_id = ht.team_id
        JOIN team at ON m.away_team_id = at.team_id
        ORDER BY pmk.recorded_at DESC;
        """
    )
except Exception as e:
    st.error(f"Database query error: {e}")
    st.info("Make sure you have run `docker compose exec django python manage.py migrate`.")
    st.stop()

if kpi_df.empty:
    st.warning("No player match KPI records found yet.")
    st.markdown(
        "Head over to the **[Django Admin Panel](/admin/)** to add a Sport, League, Season, "
        "Teams, Athletes, KPIs, Matches, and Player Match KPIs, then refresh this page."
    )
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Performance Data")

seasons = ["All Seasons"] + sorted(kpi_df["season_name"].dropna().unique().tolist())
selected_season = st.sidebar.selectbox("Season", seasons)

teams = ["All Teams"] + sorted(kpi_df["team_name"].dropna().unique().tolist())
selected_team = st.sidebar.selectbox("Team", teams)

categories = ["All Categories"] + sorted(kpi_df["kpi_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("KPI Category", categories)

filtered_df = kpi_df.copy()
if selected_season != "All Seasons":
    filtered_df = filtered_df[filtered_df["season_name"] == selected_season]
if selected_team != "All Teams":
    filtered_df = filtered_df[filtered_df["team_name"] == selected_team]
if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["kpi_category"] == selected_category]

# Top Summary Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("KPI Records", len(filtered_df))
col2.metric("Athletes Tracked", filtered_df["athlete_id"].nunique())
col3.metric("Matches Analysed", filtered_df["match_id"].nunique())

valid_targets = filtered_df.dropna(subset=["target_value"])
if not valid_targets.empty:
    hit_rate = (valid_targets["actual_value"] >= valid_targets["target_value"]).mean() * 100
    col4.metric("Target Hit Rate", f"{hit_rate:.1f}%")
else:
    col4.metric("Target Hit Rate", "N/A")

st.divider()

# Charts: Average Actual vs Target by KPI
st.subheader("Average Actual vs. Target by KPI")
summary_by_kpi = (
    filtered_df.groupby("kpi_name")[["actual_value", "target_value"]]
    .mean()
    .round(2)
)
st.bar_chart(summary_by_kpi)

# Athlete Breakdown Table
st.subheader("Recent Player Match KPI Logs")
display_cols = [
    "season_name",
    "team_name",
    "athlete_name",
    "position",
    "match_label",
    "kpi_category",
    "kpi_name",
    "actual_value",
    "target_value",
]
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
