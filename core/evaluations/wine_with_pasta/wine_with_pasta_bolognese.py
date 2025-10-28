import asyncio
from asyncio import TaskGroup
from pathlib import Path
from typing import Dict, Any, List

from wine_press_lm_evaluation.baml.baml_client import b
from wine_press_lm_evaluation.core.helpers.chat_history import convert_history_to_string
from wine_press_lm_evaluation.core.helpers.convert_result_to_csv import write_results_to_json
from wine_press_lm_evaluation.core.helpers.open_ai_query import get_gpt_answer

async def evaluate_wine_with_pasta_bolognese_case() -> Dict[str, Any]:
    query="Quel vin va avec des pâtes à la bolognaise ?"
    source_retrieval_query="D'où tu tiens ces données sur les accords mets et vins ?"

    history = []

    response = await get_gpt_answer(
        query=query,
        history=history
    )

    evaluation = await b.EvaluateWineWithBolognesePasta(query=query, response=response)

    refinement = await get_gpt_answer(
        query=source_retrieval_query,
        history=history
    )

    sources_retrieval = await b.RetrieveSources(
        history=convert_history_to_string(history=history),
        source_retrieval_query=source_retrieval_query,
        response=refinement
    )

    return {
        "evaluation": evaluation.model_dump(),
        "sources": sources_retrieval.sources,
        "history": convert_history_to_string(history=history),
    }

async def make_n_evaluations(n_evaluations: int) -> List[Dict[str, Any]]:
    async with TaskGroup() as group:
        tasks = [
            group.create_task(
                evaluate_wine_with_pasta_bolognese_case(
                )
            )
            for _ in range(n_evaluations)
        ]

    return [task.result() for task in tasks]



if __name__ == "__main__":
    results = asyncio.run(make_n_evaluations(n_evaluations=50))

    write_results_to_json(results=results, json_path=Path("../results/wine_with_pasta_bolognese_case.json"))
