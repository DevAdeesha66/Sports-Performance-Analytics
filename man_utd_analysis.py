import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_excel("man_utd_2425.xlsx")

#identify if Man United is home or away
df['ManUtdIsHome'] = df['HomeTeam'] == 'Man United'

#goal difference 
df['ManUtdGoalDiff'] = df.apply(
    lambda x: (x['FullTimeHomeGoals'] - x['FullTimeAwayGoals']) if x['ManUtdIsHome']
    else (x['FullTimeAwayGoals'] - x['FullTimeHomeGoals']), axis=1
)

# match outcome(1=win, 0=draw, -1=loss)
df['ManUtdResult'] = df.apply(
    lambda x: 1 if (x['FullTimeResult'] == 'H' and x['ManUtdIsHome']) or 
                   (x['FullTimeResult'] == 'A' and not x['ManUtdIsHome']) else
              0 if x['FullTimeResult'] == 'D' else -1, axis=1
)

# MatchDate == datetime format or not
df['MatchDate'] = pd.to_datetime(df['MatchDate'])


# Average goals scored
avg_goals_scored = df.apply(
    lambda x: x['FullTimeHomeGoals'] if x['ManUtdIsHome'] else x['FullTimeAwayGoals'], axis=1
).mean()
print(f"Average goals scored by Man United per game: {avg_goals_scored:.2f}")

# Win/Draw/Loss counts
result_counts = df['ManUtdResult'].value_counts()
print("Win/Draw/Loss Record (1=Win, 0=Draw, -1=Loss):")
print(result_counts)

# Home v Away performance
home_games = df[df['ManUtdIsHome']]
away_games = df[df['ManUtdIsHome']]
print(f"Home Games - Avg Shots: {home_games['HomeShots'].mean():.2f}")
print(f"Away Games - Avg Shots: {away_games['AwayShots'].mean():.2f}")


#points over the season
df['Points'] = df['ManUtdResult'].map({1: 3, 0: 1, -1: 0})
df['CumulativePoints'] = df['Points'].cumsum()

plt.figure(figsize=(10, 6))
plt.plot(df['MatchDate'], df['CumulativePoints'], marker='o')
plt.title("Manchester United Cumulative Points (2024/25 Season)")
plt.xlabel("Match Date")
plt.ylabel("Cumulative Points")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cumulative_points.png")
plt.show()

#goals scored and conceded
goals_scored = df.apply(
    lambda x: x['FullTimeHomeGoals'] if x['ManUtdIsHome'] else x['FullTimeAwayGoals'], axis=1
).sum()
goals_conceded = df.apply(
    lambda x: x['FullTimeAwayGoals'] if x['ManUtdIsHome'] else x['FullTimeHomeGoals'], axis=1
).sum()

plt.figure(figsize=(8, 5))
sns.barplot(x=['Goals Scored', 'Goals Conceded'], y=[goals_scored, goals_conceded])
plt.title("Manchester United Goals Scored vs. Conceded (2024/25 Season)")
plt.ylabel("Total Goals")
plt.savefig("goals_comparison.png")
plt.show()

#average of goals scored
df['ManUtdGoals'] = df.apply(
    lambda x: x['FullTimeHomeGoals'] if x['ManUtdIsHome'] else x['FullTimeAwayGoals'], axis=1
)
df['GoalsMovingAvg'] = df['ManUtdGoals'].rolling(window=5).mean()

plt.figure(figsize=(10, 6))
plt.plot(df['MatchDate'], df['GoalsMovingAvg'], marker='o')
plt.title("Manchester United 5-Game Moving Average Goals Scored")
plt.xlabel("Match Date")
plt.ylabel("Goals (Moving Average)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("goals_moving_avg.png") 
plt.show()


