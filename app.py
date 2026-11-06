from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

try:
    from nba_api.stats.endpoints import leaguegamelog
    from nba_api.stats.static import teams as nba_teams
except ImportError:
    leaguegamelog = None
    nba_teams = None

TEAM_COLUMNS = ["date", "team", "opponent", "points", "opponent_points"]
PLAYER_COLUMNS = ["date", "player", "team", "opponent", "minutes", "points", "assists", "rebounds", "blocks"]
PLAYER_STATS = ["points", "assists", "rebounds", "blocks"]
STAT_LABELS = {"points": "Punti", "assists": "Assist", "rebounds": "Rimbalzi", "blocks": "Stoppate"}

st.set_page_config(page_title="NBA Match Analyzer", page_icon="🏀", layout="wide")
st.title("🏀 Analisi NBA")
st.caption("Dati recenti quando la fonte pubblica è disponibile. Le stime sono statistiche descrittive, non certezze né consigli di scommessa.")


def current_nba_season(today=None):
    today = today or datetime.now()
    start_year = today.year if today.month >= 10 else today.year - 1
    return f"{start_year}-{str(start_year + 1)[-2:]}"


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_season_data(season):
    """Fetch team and player game logs in two league-wide requests, then join opponents by game ID."""
    if leaguegamelog is None or nba_teams is None:
        raise RuntimeError("Manca la libreria nba_api. Installa i requisiti del progetto.")

    team_log = leaguegamelog.LeagueGameLog(
        player_or_team_abbreviation="T",
        season=season,
        season_type_all_star="Regular Season",
    ).get_data_frames()[0]
    player_log = leaguegamelog.LeagueGameLog(
        player_or_team_abbreviation="P",
        season=season,
        season_type_all_star="Regular Season",
    ).get_data_frames()[0]

    if team_log.empty:
        raise RuntimeError(f"La fonte NBA non ha ancora dati di regular season per {season}.")

    team_lookup = {int(t["id"]): t["full_name"] for t in nba_teams.get_teams()}
    team_log = team_log.copy()
    team_log["TEAM_ID"] = pd.to_numeric(team_log["TEAM_ID"], errors="coerce")
    team_log["PTS"] = pd.to_numeric(team_log["PTS"], errors="coerce")
    scores = team_log.set_index(["GAME_ID", "TEAM_ID"])["PTS"]

    rows = []
    for _, row in team_log.iterrows():
        team_id = int(row["TEAM_ID"])
        game_id = row["GAME_ID"]
        opponents = team_log[(team_log["GAME_ID"] == game_id) & (team_log["TEAM_ID"] != team_id)]
        if opponents.empty:
            continue
        opponent = opponents.iloc[0]
        matchup = str(row.get("MATCHUP", ""))
        rows.append({
            "date": row.get("GAME_DATE"),
            "team": team_lookup.get(team_id, row.get("TEAM_NAME", str(team_id))),
            "opponent": team_lookup.get(int(opponent["TEAM_ID"]), opponent.get("TEAM_NAME", "Sconosciuta")),
            "points": row.get("PTS"),
            "opponent_points": scores.get((game_id, int(opponent["TEAM_ID"])), np.nan),
            "home_away": "away" if " @ " in matchup else "home",
        })

    teams = pd.DataFrame(rows)
    players = player_log.rename(columns={
        "PLAYER_NAME": "player", "TEAM_ID": "team_id", "TEAM_NAME": "team",
        "GAME_DATE": "date", "MATCHUP": "matchup", "MIN": "minutes",
        "PTS": "points", "AST": "assists", "REB": "rebounds", "BLK": "blocks",
    }).copy()
    if players.empty:
        raise RuntimeError(f"Nessuna statistica giocatore disponibile per {season}.")

    # Prefer the official team abbreviation/name already present in the league player log.
    team_name_by_abbr = {}
    for t in nba_teams.get_teams():
        team_name_by_abbr[t["abbreviation"]] = t["full_name"]
    if "TEAM_ABBREVIATION" in player_log.columns:
        players["team"] = player_log["TEAM_ABBREVIATION"].map(team_name_by_abbr).fillna(players["team"])

    players["opponent"] = players["matchup"].astype(str).str.replace(r"^.*?(?: @ | vs\. )", "", regex=True)
    players = players[["date", "player", "team", "opponent", "minutes", *PLAYER_STATS]]

    for frame in (teams, players):
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
        for col in ("points", "opponent_points", "minutes", *PLAYER_STATS):
            if col in frame.columns:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")
        frame.dropna(subset=["date"], inplace=True)
        frame.sort_values("date", inplace=True)
        frame.reset_index(drop=True, inplace=True)

    if teams.empty or players.empty:
        raise RuntimeError("La fonte ha restituito dati vuoti o incompleti.")
    return teams, players, datetime.now().strftime("%d/%m/%Y %H:%M")


def read_csv_data(team_file, player_file):
    if team_file is None or player_file is None:
        raise ValueError("Per usare i CSV devi caricare entrambi i file: squadre e giocatori.")
    teams = pd.read_csv(team_file)
    players = pd.read_csv(player_file)
    for frame in (teams, players):
        frame.columns = [str(c).strip().lower() for c in frame.columns]
    missing = [f"squadre: {c}" for c in TEAM_COLUMNS if c not in teams.columns]
    missing += [f"giocatori: {c}" for c in PLAYER_COLUMNS if c not in players.columns]
    if missing:
        raise ValueError("Colonne mancanti: " + ", ".join(missing))
    if "home_away" not in teams.columns:
        teams["home_away"] = "unknown"
    for frame in (teams, players):
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
        for col in ("points", "opponent_points", "minutes", *PLAYER_STATS):
            if col in frame.columns:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")
        frame.dropna(subset=["date"], inplace=True)
        frame.sort_values("date", inplace=True)
    if teams.empty or players.empty:
        raise ValueError("I CSV non contengono righe valide.")
    return teams, players, "file CSV caricato da te"


def team_summary(team, games):
    data = games[games["team"] == team].sort_values("date")
    if data.empty:
        raise ValueError(f"Non ci sono partite per {team}.")
    scored = pd.to_numeric(data["points"], errors="coerce").dropna()
    conceded = pd.to_numeric(data["opponent_points"], errors="coerce").dropna()
    diff = scored.reset_index(drop=True) - conceded.reset_index(drop=True)
    return {
        "games": len(data), "ppg": scored.mean(), "opp_ppg": conceded.mean(),
        "last5_ppg": scored.tail(5).mean(), "last5_opp": conceded.tail(5).mean(),
        "last5_diff": diff.tail(5).mean(), "scores": scored.tail(10).reset_index(drop=True),
        "sd": max(7.0, scored.tail(15).std(ddof=0) if len(scored.tail(15)) > 1 else 12.0),
    }


def matchup_estimate(home, away, games):
    h, a = team_summary(home, games), team_summary(away, games)
    home_points = (h["last5_ppg"] + a["last5_opp"]) / 2 + 1.5
    away_points = (a["last5_ppg"] + h["last5_opp"]) / 2
    rng = np.random.default_rng(42)
    h_sim = rng.normal(home_points, h["sd"], 30000)
    a_sim = rng.normal(away_points, a["sd"], 30000)
    home_win = float(np.mean(h_sim > a_sim))
    return h, a, float(home_points), float(away_points), home_win


def player_estimate(player, team, stat, line, players):
    data = players[(players["player"].astype(str) == player) & (players["team"].astype(str) == team)].sort_values("date")
    values = pd.to_numeric(data[stat], errors="coerce").dropna()
    if values.empty:
        raise ValueError("Non ci sono statistiche valide per questo giocatore.")
    recent = values.tail(10)
    return values, recent, float(recent.mean()), float((recent > line).mean())


with st.sidebar:
    st.header("Da dove prendere i dati")
    source = st.radio("Scegli una modalità", ["Dati NBA online", "Carica i miei CSV"], index=0)
    season = current_nba_season()
    if source == "Dati NBA online":
        st.caption(f"Stagione selezionata automaticamente: {season}")
        st.caption("Serve internet. I dati pubblici possono arrivare in ritardo o non essere disponibili.")
        if st.button("Aggiorna dati NBA"):
            fetch_season_data.clear()
    else:
        team_file = st.file_uploader("File squadre CSV", type="csv")
        player_file = st.file_uploader("File giocatori CSV", type="csv")

if source == "Dati NBA online":
    try:
        with st.spinner(f"Sto scaricando le statistiche NBA della stagione {season}…"):
            teams_df, players_df, fetched_at = fetch_season_data(season)
        latest = teams_df["date"].max()
        st.success(f"Dati NBA caricati. Ultima partita nei dati: {latest:%d/%m/%Y}. Aggiornamento: {fetched_at}.")
    except Exception as exc:
        st.error(f"Non riesco a recuperare dati NBA aggiornati: {exc}")
        st.info("Controlla la connessione e riprova più tardi. In alternativa usa la modalità CSV. Non mostro dati dimostrativi spacciandoli per aggiornati.")
        st.stop()
else:
    try:
        teams_df, players_df, fetched_at = read_csv_data(team_file, player_file)
        st.info(f"Fonte dati: {fetched_at}. Ultima data nei file: {teams_df['date'].max():%d/%m/%Y}.")
    except Exception as exc:
        st.warning(str(exc))
        st.markdown("Per i CSV servono queste colonne: squadre `date,team,opponent,points,opponent_points`; giocatori `date,player,team,opponent,minutes,points,assists,rebounds,blocks`.")
        st.stop()

teams_df = teams_df.dropna(subset=["points", "opponent_points"])
if teams_df.empty:
    st.error("I dati squadra non includono i punteggi degli avversari. Non posso calcolare un confronto corretto.")
    st.stop()

st.warning("Le percentuali sono stime semplici basate sulle partite disponibili, non probabilità validate. Non garantiscono risultati né profitti.")
match_tab, player_tab, data_tab = st.tabs(["Partita", "Statistiche giocatore", "Dati"])

with match_tab:
    team_names = sorted(teams_df["team"].dropna().astype(str).unique())
    if len(team_names) < 2:
        st.error("Servono dati per almeno due squadre.")
    else:
        home = st.selectbox("Squadra in casa", team_names)
        away = st.selectbox("Squadra in trasferta", [name for name in team_names if name != home])
        try:
            home_stats, away_stats, home_pts, away_pts, home_prob = matchup_estimate(home, away, teams_df)
            c1, c2, c3 = st.columns(3)
            c1.metric(f"Punti stimati: {home}", f"{home_pts:.1f}")
            c2.metric(f"Punti stimati: {away}", f"{away_pts:.1f}")
            c3.metric("Vittoria stimata", f"{home}: {home_prob:.0%}")
            st.write(f"Totale punti stimato: **{home_pts + away_pts:.1f}**. La stima include un piccolo vantaggio casa fisso e forma delle ultime 5 partite.")
            st.subheader("Confronto forma e medie")
            comparison = pd.DataFrame({
                home: [home_stats["ppg"], home_stats["opp_ppg"], home_stats["last5_ppg"], home_stats["last5_diff"]],
                away: [away_stats["ppg"], away_stats["opp_ppg"], away_stats["last5_ppg"], away_stats["last5_diff"]],
            }, index=["Punti fatti / partita", "Punti concessi / partita", "Punti fatti ultime 5", "Differenza punti ultime 5"])
            st.dataframe(comparison, use_container_width=True)
            chart = pd.DataFrame({home: home_stats["scores"], away: away_stats["scores"]})
            st.line_chart(chart, use_container_width=True)
        except Exception as exc:
            st.error(f"Non riesco a calcolare il confronto: {exc}")

with player_tab:
    player_names = sorted(players_df["player"].dropna().astype(str).unique())
    if not player_names:
        st.info("Nessun dato giocatore disponibile.")
    else:
        selected_player = st.selectbox("Giocatore", player_names)
        player_teams = sorted(players_df.loc[players_df["player"].astype(str) == selected_player, "team"].dropna().astype(str).unique())
        if player_teams:
            selected_team = st.selectbox("Squadra", player_teams)
            stat = st.selectbox("Statistica", PLAYER_STATS, format_func=lambda value: STAT_LABELS[value])
            player_rows = players_df[(players_df["player"].astype(str) == selected_player) & (players_df["team"].astype(str) == selected_team)]
            all_values = pd.to_numeric(player_rows[stat], errors="coerce").dropna()
            default_line = float(round(all_values.tail(10).mean() if not all_values.empty else 0, 1))
            line = st.number_input(f"Soglia di {STAT_LABELS[stat]}", min_value=0.0, value=default_line, step=0.5)
            try:
                values, recent, projection, hit_rate = player_estimate(selected_player, selected_team, stat, line, players_df)
                p1, p2, p3 = st.columns(3)
                p1.metric(f"Media ultime {len(recent)} partite", f"{projection:.1f}")
                p2.metric(f"Partite sopra soglia", f"{hit_rate:.0%}")
                p3.metric("Partite nel campione", str(len(values)))
                st.caption("La frequenza sopra soglia descrive solo il campione mostrato: non è una previsione garantita della prossima partita.")
                hist = pd.DataFrame({"Partita (dalla più vecchia alla più recente)": range(1, len(recent) + 1), STAT_LABELS[stat]: recent.to_numpy()}).set_index("Partita (dalla più vecchia alla più recente)")
                st.bar_chart(hist)
            except Exception as exc:
                st.error(str(exc))

with data_tab:
    st.write(f"Stagione: **{season if source == 'Dati NBA online' else 'CSV caricato'}**")
    st.write(f"Gare squadra disponibili: **{len(teams_df)}** | righe giocatore: **{len(players_df)}**")
    st.write(f"Ultima data partite: **{teams_df['date'].max():%d/%m/%Y}**")
    st.subheader("Ultimi risultati squadra scaricati")
    st.dataframe(teams_df.sort_values("date", ascending=False).head(30), use_container_width=True)

st.caption("La modalità online richiede connessione e dipende dal servizio pubblico NBA. Se il servizio non risponde, riprova più tardi. Nessuna scommessa viene piazzata dall'app.")
