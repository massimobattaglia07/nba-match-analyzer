import numpy as np
import pandas as pd
import streamlit as st

try:
    from nba_api.stats.static import teams as nba_teams
    from nba_api.stats.endpoints import teamgamelog, playergamelog, teamroster
except Exception:  # pragma: no cover
    nba_teams = None
    teamgamelog = None
    playergamelog = None
    teamroster = None

TEAM_COLUMNS = ["date", "team", "opponent", "points", "opponent_points"]
OPTIONAL_TEAM_COLUMNS = ["home_away"]
PLAYER_COLUMNS = ["date", "player", "team", "opponent", "minutes", "points", "assists", "rebounds", "blocks"]
PLAYER_STATS = ["points", "assists", "rebounds", "blocks"]

st.set_page_config(page_title="NBA Match Analyzer", page_icon="🏀", layout="wide")
st.title("🏀 NBA Match Analyzer")
st.caption("Free NBA intelligence app for team form, player trends, and probabilistic matchup analysis.")


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

    if "home_away" in teams.columns:
        teams["home_away"] = teams["home_away"].astype(str).str.lower().str.strip()
    else:
        teams["home_away"] = "unknown"

    teams["date"] = pd.to_datetime(teams["date"], errors="coerce")
    players["date"] = pd.to_datetime(players["date"], errors="coerce")
    teams = teams.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    players = players.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return teams, players


def normalize_minutes(value):
    if pd.isna(value):
        return 0.0
    text = str(value).strip()
    if ":" in text:
        try:
            minutes, seconds = text.split(":", 1)
            return float(minutes) + float(seconds) / 60.0
        except ValueError:
            return float(text.split(":", 1)[0])
    try:
        return float(text)
    except ValueError:
        return 0.0


def weighted_recent_mean(frame, stat, window=10):
    values = pd.to_numeric(frame[stat], errors="coerce").dropna()
    if values.empty:
        return np.nan
    recent = values.tail(window)
    return 0.35 * values.mean() + 0.65 * recent.mean()


def team_summary(team_name, teams_df):
    team = teams_df[teams_df["team"].astype(str) == team_name].copy().sort_values("date").reset_index(drop=True)
    if team.empty:
        raise ValueError(f"No data available for {team_name}.")

    team["point_diff"] = pd.to_numeric(team["points"], errors="coerce") - pd.to_numeric(team["opponent_points"], errors="coerce")
    points = pd.to_numeric(team["points"], errors="coerce").dropna()
    opp = pd.to_numeric(team["opponent_points"], errors="coerce").dropna()
    recent_points = points.tail(5)
    recent_opp = opp.tail(5)
    recent_diff = team["point_diff"].dropna().tail(5)

    return {
        "team": team_name,
        "avg_points": float(points.mean()) if not points.empty else 0.0,
        "avg_opp_points": float(opp.mean()) if not opp.empty else 0.0,
        "last5_points": float(recent_points.mean()) if not recent_points.empty else 0.0,
        "last5_opp_points": float(recent_opp.mean()) if not recent_opp.empty else 0.0,
        "last5_diff": float(recent_diff.mean()) if not recent_diff.empty else 0.0,
        "pace_proxy": float((points.mean() + opp.mean()) / 2.0),
        "points_history": pd.Series(points).reset_index(drop=True),
        "opp_points_history": pd.Series(opp).reset_index(drop=True),
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
    sim_a = rng.normal(proj_a, max(5.5, a["last5_points"] * 0.14), 25000)
    sim_b = rng.normal(proj_b, max(5.5, b["last5_points"] * 0.14), 25000)
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
        (players_df["player"].astype(str) == player_name)
        & (players_df["team"].astype(str) == player_team)
    ].copy().sort_values("date")

    if player_rows.empty:
        raise ValueError("No player data available.")

    stat_series = pd.to_numeric(player_rows[stat_name], errors="coerce").dropna()
    if stat_series.empty:
        raise ValueError("No valid stat values for this player.")

    recent = stat_series.tail(10)
    projection = 0.5 * recent.mean() + 0.5 * stat_series.mean()
    sigma = max(1.0, recent.std(ddof=0) if len(recent) > 1 else 1.0)

    rng = np.random.default_rng(7)
    sims = rng.normal(projection, sigma, 25000)
    over = float(np.mean(sims > float(line_value)))

    return {
        "projection": float(projection),
        "recent_avg": float(recent.mean()),
        "games": int(len(stat_series)),
        "over_probability": float(over),
        "history": stat_series.reset_index(drop=True),
    }


def build_match_report(match_result):
    a = match_result["a_summary"]
    b = match_result["b_summary"]

    offense_edge = "" if a["avg_points"] == b["avg_points"] else (
        f"{match_result['team_a']} has the stronger scoring profile, averaging {a['avg_points']:.1f} points per game against {b['avg_points']:.1f} for {match_result['team_b']}."
        if a["avg_points"] > b["avg_points"]
        else f"{match_result['team_b']} has the stronger scoring profile, averaging {b['avg_points']:.1f} points per game against {a['avg_points']:.1f} for {match_result['team_a']}."
    )

    defense_edge = "" if a["avg_opp_points"] == b["avg_opp_points"] else (
        f"Defensively, {match_result['team_a']} is allowing {a['avg_opp_points']:.1f} while {match_result['team_b']} allows {b['avg_opp_points']:.1f}."
        if a["avg_opp_points"] < b["avg_opp_points"]
        else f"Defensively, {match_result['team_b']} is allowing {b['avg_opp_points']:.1f} while {match_result['team_a']} allows {a['avg_opp_points']:.1f}."
    )

    form_note = (
        f"Recent form favors {match_result['team_a']} ({a['last5_points']:.1f} PPG last 5) against {match_result['team_b']} ({b['last5_points']:.1f} PPG last 5)."
        if a["last5_points"] > b["last5_points"]
        else f"Recent form favors {match_result['team_b']} ({b['last5_points']:.1f} PPG last 5) against {match_result['team_a']} ({a['last5_points']:.1f} PPG last 5)."
    )

    return (
        f"{offense_edge} {defense_edge} {form_note} "
        f"Projected total is {match_result['total']:.1f}, with a win probability of {match_result['win_a']:.0%} for {match_result['team_a']} and {match_result['win_b']:.0%} for {match_result['team_b']}."
    )


def fetch_live_nba_data(season="2024-25", games_back=10):
    if nba_teams is None or teamgamelog is None or playergamelog is None or teamroster is None:
        raise ImportError("The free NBA data library is not available. Please install nba_api.")

    team_list = nba_teams.get_teams()
    team_records = []
    player_records = []

    for team in team_list:
        team_id = int(team["id"])
        try:
            log = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star="Regular Season")
            df = log.get_data_frames()[0].head(games_back).copy()
        except Exception:
            continue

        for _, row in df.iterrows():
            opp_name = str(row.get("MATCHUP", "Unknown"))
            if " @ " in opp_name:
                opp_name = opp_name.split(" @ ", 1)[1]
            elif " vs. " in opp_name.lower():
                opp_name = opp_name.split(" vs. ", 1)[1]
            team_records.append({
                "date": row.get("GAME_DATE"),
                "team": team["full_name"],
                "opponent": opp_name,
                "points": float(row.get("PTS", 0.0) or 0.0),
                "opponent_points": float(row.get("PTS", 0.0) or 0.0),
                "home_away": "home" if " @ " not in str(row.get("MATCHUP", "")) else "away",
            })

        try:
            roster = teamroster.TeamRoster(team_id=team_id)
            roster_df = roster.get_data_frames()[0].head(12)
        except Exception:
            continue

        for _, player_row in roster_df.iterrows():
            player_id = int(player_row.get("PLAYER_ID"))
            player_name = player_row.get("PLAYER")
            try:
                player_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
                pl_df = player_log.get_data_frames()[0].head(games_back).copy()
            except Exception:
                continue

            for _, pr in pl_df.iterrows():
                opp_name = str(pr.get("MATCHUP", "Unknown"))
                if " @ " in opp_name:
                    opp_name = opp_name.split(" @ ", 1)[1]
                elif " vs. " in opp_name.lower():
                    opp_name = opp_name.split(" vs. ", 1)[1]
                player_records.append({
                    "date": pr.get("GAME_DATE"),
                    "player": player_name,
                    "team": team["full_name"],
                    "opponent": opp_name,
                    "minutes": normalize_minutes(pr.get("MIN", 0)),
                    "points": float(pr.get("PTS", 0.0) or 0.0),
                    "assists": float(pr.get("AST", 0.0) or 0.0),
                    "rebounds": float(pr.get("REB", 0.0) or 0.0),
                    "blocks": float(pr.get("BLK", 0.0) or 0.0),
                })

    if not team_records or not player_records:
        raise ValueError("No live NBA data was returned for the selected season.")

    teams_df = pd.DataFrame(team_records)
    players_df = pd.DataFrame(player_records)
    teams_df["date"] = pd.to_datetime(teams_df["date"], errors="coerce")
    players_df["date"] = pd.to_datetime(players_df["date"], errors="coerce")
    teams_df = teams_df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    players_df = players_df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return teams_df, players_df


with st.sidebar:
    st.header("Data source")
    use_demo = st.checkbox("Use sample data", value=True)
    if not use_demo:
        team_file = st.file_uploader("Upload team CSV", type="csv")
        player_file = st.file_uploader("Upload player CSV", type="csv")
    else:
        team_file = None
        player_file = None

    st.markdown("---")
    st.subheader("Live free data")
    try_live = st.checkbox("Try free live NBA data", value=False)
    if try_live:
        season_choice = st.selectbox("Season", ["2024-25", "2023-24", "2022-23"], index=0)
        if st.button("Load live data"):
            try:
                live_teams, live_players = fetch_live_nba_data(season=season_choice, games_back=10)
                st.session_state["live_teams"] = live_teams
                st.session_state["live_players"] = live_players
                st.success("Live data loaded successfully.")
            except Exception as exc:
                st.warning(f"Live data fetch failed: {exc}")

    st.caption("This is a research tool, not a guaranteed profit engine.")


if use_demo:
    teams_df, players_df = load_demo_data()
elif "live_teams" in st.session_state and "live_players" in st.session_state and st.session_state["live_teams"] is not None:
    teams_df = st.session_state["live_teams"]
    players_df = st.session_state["live_players"]
else:
    try:
        teams_df, players_df = load_uploaded_data(team_file, player_file)
    except Exception as exc:
        st.error(f"Unable to load uploaded CSVs: {exc}")
        st.stop()

team_names = sorted(teams_df["team"].astype(str).unique())

matchup_tab, player_tab, data_tab = st.tabs(["Matchup", "Player props", "Data"])

with matchup_tab:
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Team A", team_names, index=0)
    with col2:
        team_b = st.selectbox("Team B", [t for t in team_names if t != team_a], index=0)

    match = estimate_team_matchup(team_a, team_b, teams_df)
    st.write(f"**Win probability:** {team_a} {match['win_a']:.0%} | {team_b} {match['win_b']:.0%}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"Expected points — {team_a}", f"{match['proj_a']:.1f}")
    c2.metric(f"Expected points — {team_b}", f"{match['proj_b']:.1f}")
    c3.metric("Projected total", f"{match['total']:.1f}")
    c4.metric("Over 220 prob", f"{match['over_total']:.0%}")

    st.info(build_match_report(match))

    st.markdown("---")
    st.subheader("Team performance snapshot")
    info_cols = st.columns(4)
    with info_cols[0]:
        st.metric(f"{team_a} PPG", f"{match['a_summary']['avg_points']:.1f}")
    with info_cols[1]:
        st.metric(f"{team_a} opp PPG", f"{match['a_summary']['avg_opp_points']:.1f}")
    with info_cols[2]:
        st.metric(f"{team_b} PPG", f"{match['b_summary']['avg_points']:.1f}")
    with info_cols[3]:
        st.metric(f"{team_b} opp PPG", f"{match['b_summary']['avg_opp_points']:.1f}")

    team_chart_df = pd.DataFrame({
        team_a: pd.to_numeric(teams_df[teams_df['team'] == team_a]['points'], errors='coerce').tail(10).reset_index(drop=True),
        team_b: pd.to_numeric(teams_df[teams_df['team'] == team_b]['points'], errors='coerce').tail(10).reset_index(drop=True),
    })
    st.line_chart(team_chart_df, use_container_width=True)

with player_tab:
    players = sorted(players_df["player"].astype(str).unique())
    player_name = st.selectbox("Player", players)
    player_team = st.selectbox("Player team", sorted(players_df[players_df["player"].astype(str) == player_name]["team"].unique()))
    stat_name = st.selectbox("Statistic", PLAYER_STATS)
    line_value = st.number_input(f"Line for {stat_name}", min_value=0.0, value=20.0, step=0.5)

    player_result = estimate_player_projection(player_name, player_team, players_df, stat_name, line_value)
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Projected stat", f"{player_result['projection']:.1f}")
    p2.metric("Above line", f"{player_result['over_probability']:.0%}")
    p3.metric("Recent avg", f"{player_result['recent_avg']:.1f}")
    p4.metric("Games", f"{player_result['games']}")

    hist_df = pd.DataFrame({
        "game": [str(i + 1) for i in range(len(player_result["history"]))],
        "value": player_result["history"].tolist(),
    })
    if not hist_df.empty:
        st.line_chart(hist_df.set_index("game")["value"], use_container_width=True)

    st.markdown("---")
    st.subheader("Player trend notes")
    recent_scores = pd.to_numeric(players_df[(players_df["player"] == player_name) & (players_df["team"] == player_team)][stat_name], errors="coerce").dropna().tail(5)
    if not recent_scores.empty:
        st.write(f"Last 5 games for {player_name}: {list(recent_scores.astype(float).round(1))}")
        st.write(f"Average in recent sample: {recent_scores.mean():.1f}")

with data_tab:
    st.subheader("Data preview")
    preview = st.radio("Preview", ["Teams", "Players"], horizontal=True)
    if preview == "Teams":
        st.dataframe(teams_df.head(20), use_container_width=True)
    else:
        st.dataframe(players_df.head(20), use_container_width=True)

st.markdown("---")
st.caption("Free NBA analysis app for research and exploratory decision support. It does not guarantee profits, exact outcomes, or reliable betting edges.")
