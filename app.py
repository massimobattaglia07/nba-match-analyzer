import numpy as np
import pandas as pd
import streamlit as st

TEAM_COLUMNS = ["date", "team", "opponent", "points", "opponent_points"]
PLAYER_COLUMNS = ["date", "player", "team", "opponent", "minutes", "points", "assists", "rebounds", "blocks"]
PLAYER_STATS = ["points", "assists", "rebounds", "blocks"]

st.set_page_config(page_title="NBA Match Analyzer", page_icon="🏀", layout="wide")
st.title("🏀 NBA Match Analyzer")
st.caption("Free analytics dashboard for team form, player trends, and probability-based matchup analysis.")


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


def recent_window(values, window=10):
    return pd.Series(values).tail(window).reset_index(drop=True)


def weighted_recent_mean(frame, stat, window=10):
    values = pd.to_numeric(frame[stat], errors="coerce").dropna()
    if values.empty:
        return np.nan
    recent = recent_window(values, window)
    return 0.35 * values.mean() + 0.65 * recent.mean()


def team_summary(team_name, teams_df):
    team = teams_df[teams_df["team"].astype(str) == team_name].copy().sort_values("date").reset_index(drop=True)
    if team.empty:
        raise ValueError(f"No data available for {team_name}.")

    team["point_diff"] = pd.to_numeric(team["points"], errors="coerce") - pd.to_numeric(team["opponent_points"], errors="coerce")
    last5_points = recent_window(pd.to_numeric(team["points"], errors="coerce"), 5).mean()
    last5_opp_points = recent_window(pd.to_numeric(team["opponent_points"], errors="coerce"), 5).mean()
    last5_diff = recent_window(pd.to_numeric(team["point_diff"], errors="coerce"), 5).mean()
    avg_points = team["points"].mean()
    avg_opp_points = team["opponent_points"].mean()
    rating = (avg_points - avg_opp_points) * 0.7 + last5_diff * 0.3

    return {
        "team": team_name,
        "avg_points": float(avg_points),
        "avg_opp_points": float(avg_opp_points),
        "last5_points": float(last5_points),
        "last5_opp_points": float(last5_opp_points),
        "last5_diff": float(last5_diff),
        "rating": float(rating),
        "points_history": pd.Series(pd.to_numeric(team["points"], errors="coerce").dropna()),
        "opp_points_history": pd.Series(pd.to_numeric(team["opponent_points"], errors="coerce").dropna()),
    }


def estimate_team_matchup(team_a, team_b, teams_df):
    a = team_summary(team_a, teams_df)
    b = team_summary(team_b, teams_df)

    proj_a = 0.5 * (a["last5_points"] + b["last5_opp_points"])
    proj_b = 0.5 * (b["last5_points"] + a["last5_opp_points"])

    diff = proj_a - proj_b
    win_a = 1 / (1 + np.exp(-(diff / 12.0)))
    win_b = 1 - win_a
    total = proj_a + proj_b

    rng = np.random.default_rng(42)
    sim_a = rng.normal(proj_a, max(5.5, a["last5_points"] * 0.14), 30000)
    sim_b = rng.normal(proj_b, max(5.5, b["last5_points"] * 0.14), 30000)
    over_total = float(np.mean(sim_a + sim_b > 220.0))

    return {
        "team_a": team_a,
        "team_b": team_b,
        "proj_a": float(proj_a),
        "proj_b": float(proj_b),
        "total": float(total),
        "win_a": float(win_a),
        "win_b": float(win_b),
        "over_total": float(over_total),
        "a_summary": a,
        "b_summary": b,
    }


def estimate_player_projection(player_name, player_team, players_df, stat_name, line_value):
    player_rows = players_df[
        (players_df["player"].astype(str) == player_name) & (players_df["team"].astype(str) == player_team)
    ].copy().sort_values("date").reset_index(drop=True)

    if player_rows.empty:
        raise ValueError("No data available for this player and team.")

    recent = pd.to_numeric(player_rows[stat_name], errors="coerce").dropna()
    if recent.empty:
        raise ValueError("Player stat values not available.")

    recent_10 = recent.tail(10)
    projection = 0.5 * recent_10.mean() + 0.5 * recent.mean()
    sigma = max(1.0, recent_10.std(ddof=0) if len(recent_10) > 1 else 1.0)

    rng = np.random.default_rng(7)
    sims = rng.normal(projection, sigma, 25000)
    over = float(np.mean(sims > float(line_value)))

    return {
        "player": player_name,
        "team": player_team,
        "stat": stat_name,
        "projection": float(projection),
        "line_value": float(line_value),
        "over_probability": over,
        "recent_avg": float(recent_10.mean()),
        "games": int(len(recent)),
        "history": recent.reset_index(drop=True),
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
    st.caption("This is a free analytics tool and not a guaranteed betting system.")


if use_demo:
    teams_df, players_df = load_demo_data()
else:
    try:
        teams_df, players_df = load_uploaded_data(team_file, player_file)
    except Exception as exc:
        st.error(f"Unable to load uploaded CSVs: {exc}")
        st.stop()

team_names = sorted(teams_df["team"].astype(str).unique())

st.subheader("Matchup overview")
col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("Team A", team_names, index=0)
with col2:
    team_b = st.selectbox("Team B", [t for t in team_names if t != team_a], index=0)

match = estimate_team_matchup(team_a, team_b, teams_df)

m1, m2, m3, m4 = st.columns(4)
m1.metric(f"Expected points — {team_a}", f"{match['proj_a']:.1f}")
m2.metric(f"Expected points — {team_b}", f"{match['proj_b']:.1f}")
m3.metric("Projected total", f"{match['total']:.1f}")
m4.metric("Over 220 probability", f"{match['over_total']:.0%}")

st.write(f"**Win probability:** {team_a} {match['win_a']:.0%} | {team_b} {match['win_b']:.0%}")

st.markdown("---")

team_a_summary = match["a_summary"]
team_b_summary = match["b_summary"]

a_cols = st.columns(4)
with a_cols[0]:
    st.metric(f"{team_a} PPG", f"{team_a_summary['avg_points']:.1f}")
with a_cols[1]:
    st.metric(f"{team_a} OPP PPG", f"{team_a_summary['avg_opp_points']:.1f}")
with a_cols[2]:
    st.metric(f"{team_a} last 5 diff", f"{team_a_summary['last5_diff']:.1f}")
with a_cols[3]:
    st.metric(f"{team_a} rating", f"{team_a_summary['rating']:.1f}")

b_cols = st.columns(4)
with b_cols[0]:
    st.metric(f"{team_b} PPG", f"{team_b_summary['avg_points']:.1f}")
with b_cols[1]:
    st.metric(f"{team_b} OPP PPG", f"{team_b_summary['avg_opp_points']:.1f}")
with b_cols[2]:
    st.metric(f"{team_b} last 5 diff", f"{team_b_summary['last5_diff']:.1f}")
with b_cols[3]:
    st.metric(f"{team_b} rating", f"{team_b_summary['rating']:.1f}")

st.subheader("Team trend charts")
team_chart_data = pd.DataFrame({
    team_a: team_a_summary["points_history"].tail(10).reset_index(drop=True),
    team_b: team_b_summary["points_history"].tail(10).reset_index(drop=True),
})
st.line_chart(team_chart_data, use_container_width=True)

st.subheader("Player projection")
players = sorted(players_df["player"].astype(str).unique())
player_name = st.selectbox("Player", players)
player_team = st.selectbox("Player team", sorted(players_df[players_df["player"].astype(str) == player_name]["team"].unique()))
stat_name = st.selectbox("Stat", PLAYER_STATS)
line_value = st.number_input(f"Line for {stat_name}", min_value=0.0, value=20.0, step=0.5)

player_result = estimate_player_projection(player_name, player_team, players_df, stat_name, line_value)

p1, p2, p3, p4 = st.columns(4)
p1.metric("Projected stat", f"{player_result['projection']:.1f}")
p2.metric("Above line", f"{player_result['over_probability']:.0%}")
p3.metric("Recent avg", f"{player_result['recent_avg']:.1f}")
p4.metric("Games in sample", f"{player_result['games']}")

player_history = pd.DataFrame({
    "value": player_result["history"].tolist(),
    "game": [str(i + 1) for i in range(len(player_result["history"]))],
})
st.line_chart(player_history.set_index("game")["value"], use_container_width=True)

st.subheader("Data preview")
preview_mode = st.radio("Preview", ["Teams", "Players"], horizontal=True)
if preview_mode == "Teams":
    st.dataframe(teams_df.head(20), use_container_width=True)
else:
    st.dataframe(players_df.head(20), use_container_width=True)

st.markdown("---")
st.caption("Free NBA analysis app — built for research, trend review, and probabilistic exploration. This does not guarantee profits or exact match results.")
