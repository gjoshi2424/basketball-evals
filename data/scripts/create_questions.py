import pandas as pd
import json

# Read the JSONL file
df = pd.read_json('./player-season-stats.jsonl', lines=True)

# Read existing questions
existing_questions = []
try:
    with open('data/player-season-stats-questions.jsonl', 'r') as f:
        for line in f:
            existing_questions.append(json.loads(line))
except FileNotFoundError:
    pass

new_questions = []

# 3-Point Attempt Rate (3PAr) - rows 75-99
three_par_rows = df.iloc[75:100]
for _, row in three_par_rows.iterrows():
    player = row['Player']
    three_pa = int(row['3PA'])
    fga = int(row['FGA'])
    three_par = round(row['3PAr'], 3)
    
    question = {
        "input": f"{player} has attempted {three_pa} three-point field goals and {fga} total field goals. What is his 3-point attempt rate (3PAr) as a decimal? Round to the nearest 3 decimal places.",
        "target": three_par
    }
    new_questions.append(question)

# Free Throw Rate (FTr) - rows 100-124
ftr_rows = df.iloc[100:125]
for _, row in ftr_rows.iterrows():
    player = row['Player']
    fta = int(row['FTA'])
    fga = int(row['FGA'])
    ftr = round(row['FTr'], 3)
    
    question = {
        "input": f"{player} has attempted {fta} free throws and {fga} field goals. What is his free throw rate (FTr) as a decimal? Round to the nearest 3 decimal places.",
        "target": ftr
    }
    new_questions.append(question)

# Win Shares per 48 (WS/48) - rows 125-149
ws48_rows = df.iloc[125:150]
for _, row in ws48_rows.iterrows():
    player = row['Player']
    ws = round(row['WS'], 1)
    mp = int(row['MP'])
    ws48 = round(row['WS/48'], 3)
    
    question = {
        "input": f"{player} has {ws} total win shares and has played {mp} minutes. What is his win shares per 48 minutes (WS/48) as a decimal? Round to the nearest 3 decimal places.",
        "target": ws48
    }
    new_questions.append(question)

# Combine existing and new questions
all_questions = existing_questions + new_questions

# Save all questions to JSONL file
with open('data/player-season-stats-questions.jsonl', 'w') as f:
    for question in all_questions:
        f.write(json.dumps(question) + '\n')

print(f"Successfully added {len(new_questions)} new questions. Total questions: {len(all_questions)}")
