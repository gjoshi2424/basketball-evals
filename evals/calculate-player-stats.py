from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, Sample
from inspect_ai.solver import prompt_template, generate
from inspect_ai.scorer import match

PROMPT_TEMPLATE = """
Solve the following basketball stats problem step by step. The last line of your
response should be of the form "ANSWER: $ANSWER" (without quotes) 
where $ANSWER is the answer to the problem.

{prompt}

Remember to put your answer on its own line at the end in the form
"ANSWER: $ANSWER" (without quotes) where $ANSWER is the answer to 
the problem, and you do not need to use a \\boxed command.

Reasoning:
""".strip()

def record_to_sample(record):
    question = record["input"]
    answer = str(record['target']),
    metadata={"reason": record['reason']}

    return Sample(
        input=question,
        target=answer,
        metadata=metadata
    )

@task
def basketball_stats():
    solver = [prompt_template(PROMPT_TEMPLATE), generate()]
    dataset = json_dataset("../data/player-season-stats-questions.jsonl", sample_fields=record_to_sample)
    return Task(
        dataset=dataset,
        solver=solver,
        scorer=match(numeric=True),
    )
   