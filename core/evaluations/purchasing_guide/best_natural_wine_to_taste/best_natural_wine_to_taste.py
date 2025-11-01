import asyncio
from pathlib import Path
from typing import Dict, Any

from wine_press_lm_evaluation.baml.baml_client import b
from wine_press_lm_evaluation.core.helpers.chat_history import convert_history_to_string
from wine_press_lm_evaluation.core.helpers.convert_result_to_json import (
    write_results_to_json,
)
from wine_press_lm_evaluation.core.helpers.open_ai_query import get_gpt_answer
from wine_press_lm_evaluation.core.helpers.parallel_evaluations import (
    run_parallel_execution,
)


async def run_experiment() -> Dict[str, Any]:
    query = "Les meilleurs vins naturels à goûter en 2025"
    source_retrieval_query = "D'où tu tiens ces données sur les suggestions d'achat ?"

    history = []

    response = await get_gpt_answer(query=query, history=history)

    evaluation = await b.EvaluateBestNaturalWineToTaste(query=query, response=response)

    refinement = await get_gpt_answer(query=source_retrieval_query, history=history)

    sources_retrieval = await b.RetrieveSourcesPurchasingGuide(
        history=convert_history_to_string(history=history),
        source_retrieval_query=source_retrieval_query,
        response=refinement,
    )

    return {
        "evaluation": evaluation.model_dump(),
        "sources": sources_retrieval.sources,
        "history": convert_history_to_string(history=history),
    }


if __name__ == "__main__":
    results = asyncio.run(run_parallel_execution(coro=run_experiment, n_evaluations=30))

    write_results_to_json(
        results=results, json_path=Path("results/best_natural_wine_to_taste.json")
    )
