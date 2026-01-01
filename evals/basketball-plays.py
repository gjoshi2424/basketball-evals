from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, Sample
from inspect_ai.solver import multiple_choice, system_message
from inspect_ai.scorer import choice
from inspect_ai.model import GenerateConfig

SYSTEM_MESSAGE = """
Choose the correct basketball scheme or play based on the description given.
"""


def record_to_sample(record):
    return Sample(
        input=record["input"], target=record["target"], choices=record["choices"]
    )


def sample_to_fewshot(sample):
    choices_text = "\n".join([f"{chr(65+i)}) {choice}" for i, choice in enumerate(sample.choices)])
    return (
        f"{sample.input}\n\n"
        + f"{choices_text}\n\n"
        + f"\n\nANSWER: {sample.target}"
    )


@task
def basketball_mcq_eval(fewshot=True):
    solver = [multiple_choice()]
    if fewshot:
        fewshot_data = json_dataset(
            "../data/plays-few-shot.jsonl", sample_fields=record_to_sample
        )
        fewshot_examples = [sample_to_fewshot(sample) for sample in fewshot_data]
        fewshot_text = "\n\n".join(fewshot_examples)
        full_message = f"{SYSTEM_MESSAGE}\n\nHere are some examples:\n\n{fewshot_text}"
        solver.insert(0, system_message(full_message))
    else:
        solver.insert(0, system_message(SYSTEM_MESSAGE))
    return Task(
        dataset=json_dataset("../data/plays.jsonl", sample_fields=record_to_sample),
        solver=solver,
        scorer=choice(),
        config=GenerateConfig(temperature=0.0)
    )
