# NBA Match Analyzer

A free, lightweight NBA analytics app for exploring team and player trends and generating probability-based match forecasts.

This project is designed as an MVP for a free local app. It does not guarantee winning bets or exact match outcomes. It helps you reason with historical team and player data, recent form, and basic probabilistic modeling.

## Features

- Analyze team-level performance using recent game data
- Analyze player-level trends for points, assists, rebounds and blocks
- Estimate win probabilities between two teams
- Project player stat lines against a chosen threshold
- Works without paid APIs
- Supports CSV uploads and includes sample data

## Data model

The app expects two CSV files:

1. Team data: `teams.csv`
2. Player data: `players.csv`

### Team CSV

```csv
date,team,opponent,points,opponent_points
2024-01-10,Boston Celtics,Miami Heat,120,110
2024-01-12,Miami Heat,Boston Celtics,105,112
```

### Player CSV

```csv
date,player,team,opponent,minutes,points,assists,rebounds,blocks
2024-01-10,Jayson Tatum,Boston Celtics,Miami Heat,38,31,5,9,1
2024-01-12,Tyrese Maxey,Philadelphia 76ers,Boston Celtics,35,22,7,3,1
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Notes

- This is a free MVP, not a guaranteed betting system.
- It is better used for research and analysis than for automatic decision-making.
- The app can be linked later to public NBA datasets or APIs if you want to automate the data collection step.

## Future upgrades

- Add public API integration such as balldontlie or NBA public endpoints
- Add more advanced feature engineering and model calibration
- Add user accounts and saved analyses
- Add historical season comparisons and lineups

## Important

This app is meant for educational and analytical use. It does not promise reliable profits and should not be marketed as a guaranteed prediction engine.
