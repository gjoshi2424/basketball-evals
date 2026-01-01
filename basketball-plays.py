from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, Sample
from inspect_ai.solver import multiple_choice, system_message
from inspect_ai.scorer import choice

SYSTEM_MESSAGE = """
Choose the correct basketball scheme or play based on the description given.
"""

def record_to_sample(record):
    return Sample(
        input=record["input"],
        target=record['target'],
        choices=record["choices"]
    )

@task
def basketball_mcq_eval():
    dataset=json_dataset("plays.jsonl", sample_fields=record_to_sample)
    return Task(
        dataset=dataset,
        solver=[
          system_message(SYSTEM_MESSAGE),
          multiple_choice()
        ],
        scorer=choice()
    )