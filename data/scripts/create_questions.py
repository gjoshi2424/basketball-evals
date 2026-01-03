import pandas as pd
import json

# Read the JSONL file
df = pd.read_json('../player-season-stats.jsonl', lines=True)

all_questions = []

# Effective Field Goal % (eFG%) - rows 25-49
efg_rows = df.iloc[25:50]
for _, row in efg_rows.iterrows():
    player = row['Player']
    fg = int(row['FG'])
    three_p = int(row['3P'])
    fga = int(row['FGA'])
    efg = round((fg + 0.5 * three_p) / fga, 3)
    
    reasoning = f"eFG% = (FG + 0.5 * 3P) / FGA = ({fg} + 0.5 * {three_p}) / {fga} = ({fg} + {0.5 * three_p}) / {fga} = {fg + 0.5 * three_p} / {fga} = {efg}"
    
    question = {
        "input": f"{player} has made {fg} total field goals, {three_p} three-point field goals, and has attempted {fga} field goals. What is his effective field goal percentage (eFG%) as a decimal? Round to the nearest 3 decimal places.",
        "target": efg,
        "reasoning": reasoning
    }
    all_questions.append(question)

# True Shooting % (TS%) - rows 50-74
ts_rows = df.iloc[50:75]
for _, row in ts_rows.iterrows():
    player = row['Player']
    pts = int(row['PTS'])
    fga = int(row['FGA'])
    fta = int(row['FTA'])
    ts = round(pts / (2 * (fga + 0.44 * fta)), 3)
    
    denominator_inner = fga + 0.44 * fta
    denominator = 2 * denominator_inner
    reasoning = f"TS% = PTS / (2 * (FGA + 0.44 * FTA)) = {pts} / (2 * ({fga} + 0.44 * {fta})) = {pts} / (2 * ({fga} + {round(0.44 * fta, 2)})) = {pts} / (2 * {round(denominator_inner, 2)}) = {pts} / {round(denominator, 2)} = {ts}"
    
    question = {
        "input": f"{player} has scored {pts} total points, attempted {fga} field goals, and attempted {fta} free throws. What is his true shooting percentage (TS%) as a decimal? Round to the nearest 3 decimal places.",
        "target": ts,
        "reasoning": reasoning
    }
    all_questions.append(question)

# 3-Point Attempt Rate (3PAr) - rows 75-99
three_par_rows = df.iloc[75:100]
for _, row in three_par_rows.iterrows():
    player = row['Player']
    three_pa = int(row['3PA'])
    fga = int(row['FGA'])
    three_par = round(row['3PAr'], 3)
    
    reasoning = f"3PAr = 3PA / FGA = {three_pa} / {fga} = {three_par}"
    
    question = {
        "input": f"{player} has attempted {three_pa} three-point field goals and {fga} total field goals. What is his 3-point attempt rate (3PAr) as a decimal? Round to the nearest 3 decimal places.",
        "target": three_par,
        "reasoning": reasoning
    }
    all_questions.append(question)

# Free Throw Rate (FTr) - rows 100-124
ftr_rows = df.iloc[100:125]
for _, row in ftr_rows.iterrows():
    player = row['Player']
    fta = int(row['FTA'])
    fga = int(row['FGA'])
    ftr = round(row['FTr'], 3)
    
    reasoning = f"FTr = FTA / FGA = {fta} / {fga} = {ftr}"
    
    question = {
        "input": f"{player} has attempted {fta} free throws and {fga} field goals. What is his free throw rate (FTr) as a decimal? Round to the nearest 3 decimal places.",
        "target": ftr,
        "reasoning": reasoning
    }
    all_questions.append(question)

# Win Shares per 48 (WS/48) - rows 125-149
ws48_rows = df.iloc[125:150]
for _, row in ws48_rows.iterrows():
    player = row['Player']
    ws = round(row['WS'], 1)
    mp = int(row['MP'])
    ws48 = round(row['WS/48'], 3)
    
    ws_per_minute = ws / mp
    reasoning = f"WS/48 = (WS / MP) * 48 = ({ws} / {mp}) * 48 = {round(ws_per_minute, 6)} * 48 = {ws48}"
    
    question = {
        "input": f"{player} has {ws} win shares over {mp} minutes played. What is his win shares per 48 minutes (WS/48) as a decimal? Round to the nearest 3 decimal places.",
        "target": ws48,
        "reasoning": reasoning
    }
    all_questions.append(question)

# Save all questions to JSONL file
with open('../player-season-stats-questions.jsonl', 'w') as f:
    for question in all_questions:
        f.write(json.dumps(question) + '\n')

print(f"Successfully created {len(all_questions)} questions")
