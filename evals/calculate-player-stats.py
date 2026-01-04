from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset, Sample
from inspect_ai.solver import prompt_template, generate, use_tools
from inspect_ai.scorer import match
from inspect_ai.model import GenerateConfig
from inspect_ai.tool import tool


PROMPT_TEMPLATE = """
Solve the following basketball stats problem step by step. You can use the given tools and trust the result from them. The last line of your
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
    answer = str(record['target'])
    metadata = {"reason": record['reasoning']}

    return Sample(
        input=question,
        target=answer,
        metadata=metadata
    )

@tool
def efg():
    async def execute(FG: str, FGA: str, three_P: str):
        """
        Calculate effective field goal percentage.

        Args:
            FG: Total field goals made.
            FGA: Total field goals attempted.
            three_P: Three-point field goals made.

        Returns:
            The effective field goal percentage rounded to 3 decimal places.
        """
        return round((float(FG) + 0.5 * float(three_P)) / float(FGA), 3)

    return execute

@tool
def true_shooting():
    async def execute(PTS: str, FGA: str, FTA: str):
        """
        Calculate true shooting percentage.

        Args:
            PTS: Total points scored.
            FGA: Total field goals attempted.
            FTA: Total free throws attempted.

        Returns:
            The true shooting percentage rounded to 3 decimal places.
        """
        pts = float(PTS)
        fga = float(FGA)
        fta = float(FTA)
        return round(pts / (2 * (fga + 0.44 * fta)), 3)

    return execute

@tool
def three_point_attempt_rate():
    async def execute(three_PA: str, FGA: str):
        """
        Calculate 3-point attempt rate.

        Args:
            three_PA: Three-point field goals attempted.
            FGA: Total field goals attempted.

        Returns:
            The 3-point attempt rate rounded to 3 decimal places.
        """
        return round(float(three_PA) / float(FGA), 3)

    return execute

@tool
def free_throw_rate():
    async def execute(FTA: str, FGA: str):
        """
        Calculate free throw rate.

        Args:
            FTA: Total free throws attempted.
            FGA: Total field goals attempted.

        Returns:
            The free throw rate rounded to 3 decimal places.
        """
        return round(float(FTA) / float(FGA), 3)

    return execute


@task
def basketball_stats():
    solver = [prompt_template(PROMPT_TEMPLATE), use_tools(efg(), true_shooting(), three_point_attempt_rate(), free_throw_rate()), generate()]
    dataset = json_dataset("../data/player-season-stats-questions.jsonl", sample_fields=record_to_sample)
    return Task(
        dataset=dataset,
        solver=solver,
        scorer=match(numeric=True),
        config=GenerateConfig(temperature=0.0)
    )
   