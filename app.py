import numpy as np
import pandas as pd
import streamlit as st

TEAM_COLUMNS = ["date", "team", "opponent", "points", "opponent_points"]
PLAYER_COLUMNS = ["date", "player", "team", "opponent", "minutes", "points", "assists", "rebounds", "blocks"]
PLAYER_STATS = ["points", "assists", "rebounds", "blocks"]

st.set_page_config(page_title="NBA Match Analyzer", page_icon="🏀")
st.title("🏀 NBA Match Analyzer")
st.caption("Free MVP for team and player trend analysis and matchup probability estimates.")


@st.cache_data
def load_demo_data():
    teams = pd.DataFrame(
        [
            {"date": "2024-01-01", "team": "Boston Celtics", "opponent": "Miami Heat", "points": 120, "opponent_points": 112},
            {"date": "2024-01-04", "team": "Boston Celtics", "opponent": "New York Knicks", "points": 118, "opponent_points": 108},
            {"date": "2024-01-07", "team": "Boston Celtics", "opponent": "Toronto Raptors", "points": 126, "opponent_points": 111},
            {"date": "2024-01-10", "team": "Boston Celtics", "opponent": "Milwaukee Bucks", "points": 114, "opponent_points": 116},
            {"date": "2024-01-12", "team": "Boston Celtics", "opponent": "Cleveland Cavaliers", "points": 121, "opponent_points": 110},
            {"date": "2024-01-15", "team": "Boston Celtics", "opponent": "Chicago Bulls", "points": 123, "opponent_points": 101},
            {"date": "2024-01-02", "team": "Miami Heat", "opponent": "Boston Celtics", "points": 109, "opponent_points": 115},
            {"date": "2024-01-05", "team": "Miami Heat", "opponent": "Atlanta Hawks", "points": 110, "opponent_points": 105},
            {"date": "2024-01-08", "team": "Miami Heat", "opponent": "Toronto Raptors", "points": 112, "opponent_points": 107},
            {"date": "2024-01-11", "team": "Miami Heat", "opponent": "Brooklyn Nets", "points": 104, "opponent_points": 99},
            {"date": "2024-01-14", "team": "Miami Heat", "opponent": "New York Knicks", "points": 108, "opponent_points": 111},
            {"date": "2024-01-16", "team": "Miami Heat", "opponent": "Orlando Magic", "points": 117, "opponent_points": 106},
            {"date": "2024-01-03", "team": "Los Angeles Lakers", "opponent": "Golden State Warriors", "points": 116, "opponent_points": 119},
            {"date": "2024-01-06", "team": "Los Angeles Lakers", "opponent": "Phoenix Suns", "points": 122, "opponent_points": 118},
            {"date": "2024-01-09", "team": "Los Angeles Lakers", "opponent": "Minnesota Timberwolves", "points": 119, "opponent_points": 122},
            {"date": "2024-01-11", "team": "Los Angeles Lakers", "opponent": "Sacramento Kings", "points": 124, "opponent_points": 116},
            {"date": "2024-01-13", "team": "Los Angeles Lakers", "opponent": "Dallas Mavericks", "points": 110, "opponent_points": 113},
            {"date": "2024-01-17", "team": "Los Angeles Lakers", "opponent": "Oklahoma City Thunder", "points": 122, "opponent_points": 117},
            {"date": "2024-01-04", "team": "Golden State Warriors", "opponent": "Los Angeles Lakers", "points": 118, "opponent_points": 114},
            {"date": "2024-01-07", "team": "Golden State Warriors", "opponent": "Phoenix Suns", "points": 115, "opponent_points": 110},
            {"date": "2024-01-10", "team": "Golden State Warriors", "opponent": "Sacramento Kings", "points": 112, "opponent_points": 109},
            {"date": "2024-01-12", "team": "Golden State Warriors", "opponent": "Portland Trail Blazers", "points": 120, "opponent_points": 108},
            {"date": "2024-01-15", "team": "Golden State Warriors", "opponent": "Houston Rockets", "points": 121, "opponent_points": 118},
            {"date": "2024-01-18", "team": "Golden State Warriors", "opponent": "Denver Nuggets", "points": 108, "opponent_points": 114},
        ]
    )

    players = pd.DataFrame(
        [
            {"date": "2024-01-01", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "Miami Heat", "minutes": 38, "points": 31, "assists": 5, "rebounds": 9, "blocks": 1},
            {"date": "2024-01-04", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "New York Knicks", "minutes": 39, "points": 34, "assists": 7, "rebounds": 8, "blocks": 1},
            {"date": "2024-01-07", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "Toronto Raptors", "minutes": 37, "points": 29, "assists": 6, "rebounds": 10, "blocks": 2},
            {"date": "2024-01-10", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "Milwaukee Bucks", "minutes": 40, "points": 27, "assists": 8, "rebounds": 11, "blocks": 1},
            {"date": "2024-01-12", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "Cleveland Cavaliers", "minutes": 35, "points": 33, "assists": 5, "rebounds": 7, "blocks": 2},
            {"date": "2024-01-15", "player": "Jayson Tatum", "team": "Boston Celtics", "opponent": "Chicago Bulls", "minutes": 36, "points": 28, "assists": 9, "rebounds": 8, "blocks": 1},
            {"date": "2024-01-02", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "Boston Celtics", "minutes": 37, "points": 27, "assists": 4, "rebounds": 7, "blocks": 1},
            {"date": "2024-01-05", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "Atlanta Hawks", "minutes": 35, "points": 24, "assists": 6, "rebounds": 6, "blocks": 0},
            {"date": "2024-01-08", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "Toronto Raptors", "minutes": 36, "points": 26, "assists": 7, "rebounds": 8, "blocks": 1},
            {"date": "2024-01-11", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "Brooklyn Nets", "minutes": 34, "points": 22, "assists": 5, "rebounds": 5, "blocks": 1},
            {"date": "2024-01-14", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "New York Knicks", "minutes": 38, "points": 29, "assists": 8, "rebounds": 9, "blocks": 1},
            {"date": "2024-01-16", "player": "Jimmy Butler", "team": "Miami Heat", "opponent": "Orlando Magic", "minutes": 39, "points": 30, "assists": 7, "rebounds": 10, "blocks": 2},
            {"date": "2024-01-03", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Golden State Warriors", "minutes": 39, "points": 33, "assists": 9, "rebounds": 8, "blocks": 1},
            {"date": "2024-01-06", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Phoenix Suns", "minutes": 37, "points": 30, "assists": 11, "rebounds": 7, "blocks": 1},
            {"date": "2024-01-09", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Minnesota Timberwolves", "minutes": 38, "points": 28, "assists": 10, "rebounds": 9, "blocks": 2},
            {"date": "2024-01-11", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Sacramento Kings", "minutes": 40, "points": 35, "assists": 12, "rebounds": 8, "blocks": 1},
            {"date": "2024-01-13", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Dallas Mavericks", "minutes": 36, "points": 31, "assists": 9, "rebounds": 10, "blocks": 2},
            {"date": "2024-01-17", "player": "LeBron James", "team": "Los Angeles Lakers", "opponent": "Oklahoma City Thunder", "minutes": 37, "points": 32, "assists": 8, "rebounds": 7, "blocks": 1},
            {"date": "2024-01-04", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Los Angeles Lakers", "minutes": 35, "points": 32, "assists": 10, "rebounds": 5, "blocks": 0},
            {"date": "2024-01-07", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Phoenix Suns", "minutes": 36, "points": 28, "assists": 8, "rebounds": 4, "blocks": 1},
            {"date": "2024-01-10", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Sacramento Kings", "minutes": 37, "points": 30, "assists": 9, "rebounds": 6, "blocks": 1},
            {"date": "2024-01-12", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Portland Trail Blazers", "minutes": 34, "points": 29, "assists": 7, "rebounds": 5, "blocks": 0},
            {"date": "2024-01-15", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Houston Rockets", "minutes": 38, "points": 35, "assists": 11, "rebounds": 6, "blocks": 1},
            {"date": "2024-01-18", "player": "Stephen Curry", "team": "Golden State Warriors", "opponent": "Denver Nuggets", "minutes": 39, "points": 31, "assists": 10, "rebounds": 5, "blocks": 1},
        ]
    )
    teams["date"] = pd.to_datetime(teams["date"])
    players["date"] = pd.to_datetime(players["date"])
    return teams, players


def load_uploaded_data(team_upload, player_upload):
    if team_upload is None or player_upload is None:
        raise ValueError("Upload both CSV files.")

    teams = pd.read_csv(team_upload)
    players = pd.read_csv(player_upload)

    for frame in (teams, players):
        frame.columns = [str(c).strip().lower() for c in frame.columns]

    missing_teams = [col for col in TEAM_COLUMNS if col not in teams.columns]
    missing_players = [col for col in PLAYER_COLUMNS if col not in players.columns]

    if missing_teams or missing_players:
        missing = ", ".join(missing_teams + missing_players)
        raise ValueError(f"Missing required columns: {missing}")

    teams["date"] = pd.to_datetime(teams["date"], errors="coerce")
    players["date"] = pd.to_datetime(players["date"], errors="coerce")
    teams = teams.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    players = players.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return teams, players


def weighted_recent_mean(frame, stat):
    values = pd.to_numeric(frame[stat], errors="coerce").dropna()
    if values.empty:
        return np.nan
    recent = values.tail(min(10, len(values)))
    return 0.35 * values.mean() + 0.65 * recent.mean()


def estimate_team_matchup(team_a, team_b, teams_df):
    a = teams_df[teams_df["team"].astype(str) == team_a].copy()
    b = teams_df[teams_df["team"].astype(str) == team_b].copy()

    if a.empty or b.empty:
        raise ValueError("Missing data for one or both teams.")

    pred_a = np.mean([
        weighted_recent_mean(a, "points"),
        weighted_recent_mean(b, "opponent_points"),
    ])
    pred_b = np.mean([
        weighted_recent_mean(b, "points"),
        weighted_recent_mean(a, "opponent_points"),
    ])

    sigma_a = max(6.0, a["points"].std(ddof=0) if not a["points"].dropna().empty else 6.0)
    sigma_b = max(6.0, b["points"].std(ddof=0) if not b["points"].dropna().empty else 6.0)

    rng = np.random.default_rng(42)
    sim_a = rng.normal(pred_a, sigma_a, 25000)
    sim_b = rng.normal(pred_b, sigma_b, 25000)

    win_a = float(np.mean(sim_a > sim_b))
    win_b = float(np.mean(sim_b > sim_a))
    over_total = float(np.mean((sim_a + sim_b) > 220.0))

    return {
        "pred_a": float(pred_a),
        "pred_b": float(pred_b),
        "win_a": win_a,
        "win_b": win_b,
        "over_total": over_total,
        "team_a_avg": float(a["points"].mean()),
        "team_b_avg": float(b["points"].mean()),
        "team_a_opponent_avg": float(a["opponent_points"].mean()),
        "team_b_opponent_avg": float(b["opponent_points"].mean()),
    }


def estimate_player_projection(player_name, team_name, players_df, stat_name, line_value):
    player_rows = players_df[(players_df["player"].astype(str) == player_name) & (players_df["team"].astype(str) == team_name)].copy()
    if player_rows.empty:
        raise ValueError("No data for this player and team.")

    projection = weighted_recent_mean(player_rows, stat_name)
    recent = pd.to_numeric(player_rows[stat_name], errors="coerce").dropna().tail(10)
    sigma = float(max(1.0, recent.std(ddof=0) if len(recent) > 1 else 1.0))

    rng = np.random.default_rng(7)
    sims = rng.normal(projection, sigma, 20000)
    over = float(np.mean(sims > line_value))

    return {
        "projection": float(projection),
        "stat_name": stat_name,
        "line_value": float(line_value),
        "over_probability": over,
        "recent_avg": float(recent.mean()) if not recent.empty else float(projection),
        "games": int(len(player_rows)),
    }


with st.sidebar:
    st.header("Input")
    use_demo = st.checkbox("Use sample data", value=True)

    if not use_demo:
        team_file = st.file_uploader("Upload team CSV", type="csv")
        player_file = st.file_uploader("Upload player CSV", type="csv")
    else:
        team_file = None
        player_file = None

    st.caption("This is a free analysis tool. It does not guarantee wins or exact outcomes.")


if use_demo:
    teams_df, players_df = load_demo_data()
else:
    try:
        teams_df, players_df = load_uploaded_data(team_file, player_file)
    except Exception as exc:
        st.error(f"Unable to load uploaded CSVs: {exc}")
        st.stop()

team_names = sorted(teams_df["team"].astype(str).unique())

st.subheader("Team matchup analysis")
col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("Team A", team_names, index=0)
with col2:
    team_b = st.selectbox("Team B", [t for t in team_names if t != team_a], index=0)

try:
    result = estimate_team_matchup(team_a, team_b, teams_df)
except Exception as exc:
    st.error(f"Matchup estimation failed: {exc}")
    st.stop()

m1, m2, m3 = st.columns(3)
m1.metric(f"Expected points — {team_a}", f"{result['pred_a']:.1f}")
m2.metric(f"Expected points — {team_b}", f"{result['pred_b']:.1f}")
m3.metric("Projected total", f"{result['pred_a'] + result['pred_b']:.1f}")

st.write(f"**Win probability:** {team_a} {result['win_a']:.0%} | {team_b} {result['win_b']:.0%}")

with st.expander("Reasoning"):
    st.write(
        f"{team_a} has averaged {result['team_a_avg']:.1f} points in the sample, while {team_b} has allowed {result['team_b_opponent_avg']:.1f} per game on average. "
        f"{team_b} has averaged {result['team_b_avg']:.1f} points, while {team_a} has allowed {result['team_a_opponent_avg']:.1f} points per game. "
        "This is a simple trend-based estimate, not a guarantee."
    )

st.subheader("Player projection")
players = sorted(players_df["player"].astype(str).unique())
player_name = st.selectbox("Player", players)
player_team = st.selectbox("Player team", sorted(players_df[players_df["player"].astype(str) == player_name]["team"].unique()))
stat_name = st.selectbox("Statistic", PLAYER_STATS)
line_value = st.number_input(f"Line for {stat_name}", min_value=0.0, value=20.0, step=0.5)

player_result = estimate_player_projection(player_name, player_team, players_df, stat_name, line_value)

pp1, pp2, pp3 = st.columns(3)
pp1.metric(f"Projected {stat_name}", f"{player_result['projection']:.1f}")
pp2.metric("Above line", f"{player_result['over_probability']:.0%}")
pp3.metric("Games in sample", f"{player_result['games']}")

st.caption("This forecast uses recent game form and a simple probability simulation. It is better used for hypothesis testing than for certainty.")

st.subheader("Raw data preview")
preview_mode = st.radio("Preview", ["Teams", "Players"], horizontal=True)
if preview_mode == "Teams":
    st.dataframe(teams_df.head(20), use_container_width=True)
else:
    st.dataframe(players_df.head(20), use_container_width=True)

st.markdown("---")
st.caption("Free NBA analysis app — for research and documentation only. Not a guaranteed winning system.")
