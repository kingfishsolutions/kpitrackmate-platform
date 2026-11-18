import os
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

# Page configuration
st.set_page_config(
    page_title="Player KPI Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------
# 1. Database Connection (SQLAlchemy)
# ---------------------------------------------------------
@st.cache_resource
def get_engine():
    db_user = os.getenv("POSTGRES_USER", os.getenv("DB_USER", "postgres"))
    db_pass = os.getenv("POSTGRES_PASSWORD", os.getenv("DB_PASSWORD", "postgres"))
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", os.getenv("DB_NAME", "postgres"))
    
    connection_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_url)

engine = get_engine()

# ---------------------------------------------------------
# 2. Data Loading Helpers (Update table/column names as needed)
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def load_teams():
    query = "SELECT id, name FROM core_team ORDER BY name"
    try:
        return pd.read_sql_query(query, engine)
    except Exception:
        # Fallback sample data if tables aren't populated yet
        return pd.DataFrame({"id": [1, 2], "name": ["Melbourne United", "Hawthorn Hawks"]})

@st.cache_data(ttl=60)
def load_seasons():
    query = "SELECT id, name FROM core_season ORDER BY name DESC"
    try:
        return pd.read_sql_query(query, engine)
    except Exception:
        return pd.DataFrame({"id": list((1, 2)), "name": ["2026 Season", "2025 Season"]})

@st.cache_data(ttl=60)
def load_players(team_id: int, season_id: int):
    query = text("""
        SELECT DISTINCT p.id, p.first_name || ' ' || p.last_name AS full_name
        FROM core_player p
        JOIN core_roster r ON r.player_id = p.id
        WHERE r.team_id = :team_id AND r.season_id = :season_id
        ORDER BY full_name
    """)
    try:
        return pd.read_sql_query(query, engine, params={"team_id": int(team_id), "season_id": int(season_id)})
    except Exception:
        return pd.DataFrame({"id": list((1, 2)), "full_name": ["Alex Mercer", "Jordan Taylor"]})

@st.cache_data(ttl=60)
def load_player_kpis(player_id: int, season_id: int):
    query = text("""
        SELECT 
            g.game_date,
            g.round_number,
            g.opponent,
            CONCAT('R', g.round_number, ' vs ', g.opponent) AS game_label,
            k.category AS kpi_category,
            k.name AS kpi_name,
            pk.value AS kpi_value
        FROM core_playerkpi pk
        JOIN core_game g ON pk.game_id = g.id
        JOIN core_kpi k ON pk.kpi_id = k.id
        WHERE pk.player_id = :player_id AND g.season_id = :season_id
        ORDER BY g.game_date ASC, g.round_number ASC
    """)
    try:
        return pd.read_sql_query(query, engine, params={"player_id": int(player_id), "season_id": int(season_id)})
    except Exception:
        # Realistic mock dataset so the dashboard renders immediately during setup
        return pd.DataFrame([
            {"game_date": "2026-03-14", "round_number": 1, "opponent": "Geelong", "game_label": "R1 vs Geelong", "kpi_category": "Attack", "kpi_name": "Disposals", "kpi_value": 24},
            {"game_date": "2026-03-14", "round_number": 1, "opponent": "Geelong", "game_label": "R1 vs Geelong", "kpi_category": "Attack", "kpi_name": "Inside 50s", "kpi_value": 5},
            {"game_date": "2026-03-14", "round_number": 1, "opponent": "Geelong", "game_label": "R1 vs Geelong", "kpi_category": "Defence", "kpi_name": "Tackles", "kpi_value": 6},
            {"game_date": "2026-03-21", "round_number": 2, "opponent": "Sydney", "game_label": "R2 vs Sydney", "kpi_category": "Attack", "kpi_name": "Disposals", "kpi_value": 29},
            {"game_date": "2026-03-21", "round_number": 2, "opponent": "Sydney", "game_label": "R2 vs Sydney", "kpi_category": "Attack", "kpi_name": "Inside 50s", "kpi_value": 7},
            {"game_date": "2026-03-21", "round_number": 2, "opponent": "Sydney", "game_label": "R2 vs Sydney", "kpi_category": "Defence", "kpi_name": "Tackles", "kpi_value": 4},
            {"game_date": "2026-03-28", "round_number": 3, "opponent": "Brisbane", "game_label": "R3 vs Brisbane", "kpi_category": "Attack", "kpi_name": "Disposals", "kpi_value": 21},
            {"game_date": "2026-03-28", "round_number": 3, "opponent": "Brisbane", "game_label": "R3 vs Brisbane", "kpi_category": "Attack", "kpi_name": "Inside 50s", "kpi_value": 4},
            {"game_date": "2026-03-28", "round_number": 3, "opponent": "Brisbane", "game_label": "R3 vs Brisbane", "kpi_category": "Defence", "kpi_name": "Tackles", "kpi_value": 9},
            {"game_date": "2026-04-04", "round_number": 4, "opponent": "Carlton", "game_label": "R4 vs Carlton", "kpi_category": "Attack", "kpi_name": "Disposals", "kpi_value": 32},
            {"game_date": "2026-04-04", "round_number": 4, "opponent": "Carlton", "game_label": "R4 vs Carlton", "kpi_category": "Attack", "kpi_name": "Inside 50s", "kpi_value": 8},
            {"game_date": "2026-04-04", "round_number": 4, "opponent": "Carlton", "game_label": "R4 vs Carlton", "kpi_category": "Defence", "kpi_name": "Tackles", "kpi_value": 7},
        ])

# ---------------------------------------------------------
# 3. Navigation Sidebar
# ---------------------------------------------------------
st.sidebar.image("http://localhost/static/images/logo.jpg", use_container_width=True)
st.sidebar.title("KPI TrackMate")
screen = st.sidebar.radio(
    "Navigation",
    options=[
        "Screen 1: Season Player Performance",
        "Screen 2: Game Breakdown",
    ],
)

# ---------------------------------------------------------
# 4. Screen 1: Season Player Performance
# ---------------------------------------------------------
if screen == "Screen 1: Season Player Performance":
    st.title("Season Player Performance")
    st.markdown("Track individual player KPI trends across every game in the selected season.")

    # Top Selection Dropdowns: Team, Season, Player
    col1, col2, col3 = st.columns(3)

    teams_df = load_teams()
    with col1:
        selected_team_name = st.selectbox(
            "Select Team",
            options=teams_df["name"].tolist() if not teams_df.empty else [],
        )
        selected_team_id = (
            teams_df.loc[teams_df["name"] == selected_team_name, "id"].values[0]
            if selected_team_name
            else None
        )

    seasons_df = load_seasons()
    with col2:
        selected_season_name = st.selectbox(
            "Select Season",
            options=seasons_df["name"].tolist() if not seasons_df.empty else [],
        )
        selected_season_id = (
            seasons_df.loc[seasons_df["name"] == selected_season_name, "id"].values[0]
            if selected_season_name
            else None
        )

    players_df = (
        load_players(selected_team_id, selected_season_id)
        if selected_team_id and selected_season_id
        else pd.DataFrame()
    )
    with col3:
        selected_player_name = st.selectbox(
            "Select Player",
            options=players_df["full_name"].tolist() if not players_df.empty else [],
        )
        selected_player_id = (
            players_df.loc[players_df["full_name"] == selected_player_name, "id"].values[0]
            if selected_player_name
            else None
        )

    st.divider()

    # Load and Filter KPI Data
    if selected_player_id and selected_season_id:
        kpi_df = load_player_kpis(selected_player_id, selected_season_id)

        if kpi_df.empty:
            st.info("No KPI records found for this player in the selected season.")
        else:
            # KPI Filters: Category & Individual KPI
            filter_col1, filter_col2 = st.columns(2)

            all_categories = sorted(kpi_df["kpi_category"].dropna().unique().tolist())
            with filter_col1:
                selected_categories = st.multiselect(
                    "Filter by Category",
                    options=all_categories,
                    default=all_categories,
                    placeholder="Choose one or more categories...",
                )

            # Restrict available KPIs based on selected categories
            category_filtered_df = kpi_df[kpi_df["kpi_category"].isin(selected_categories)]
            available_kpis = sorted(category_filtered_df["kpi_name"].dropna().unique().tolist())

            with filter_col2:
                selected_kpis = st.multiselect(
                    "Filter by Individual KPI",
                    options=available_kpis,
                    default=available_kpis,
                    placeholder="Choose specific KPIs to display...",
                )

            final_df = category_filtered_df[category_filtered_df["kpi_name"].isin(selected_kpis)]

            if final_df.empty:
                st.warning("Select at least one category and one KPI to display the performance chart.")
            else:
                # Linear Graph of Player Progress Over the Season
                fig = px.line(
                    final_df,
                    x="game_label",
                    y="kpi_value",
                    color="kpi_name",
                    markers=True,
                    line_dash="kpi_category",
                    hover_data={
                        "game_date": True,
                        "kpi_category": True,
                        "kpi_name": True,
                        "kpi_value": True,
                        "game_label": False,
                    },
                    labels={
                        "game_label": "Game",
                        "kpi_value": "KPI Value",
                        "kpi_name": "KPI",
                        "kpi_category": "Category",
                        "game_date": "Date",
                    },
                )
