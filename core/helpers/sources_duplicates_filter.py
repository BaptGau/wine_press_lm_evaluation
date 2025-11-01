from typing import List

from wine_press_lm_evaluation.baml.baml_client import b
from wine_press_lm_evaluation.baml.baml_client.type_builder import TypeBuilder


TREATED_CONSTANT = "Treated"  # to be used to mark that sources were processed


async def remove_sources_duplicates(sources: List[str]) -> List[str]:
    """
    Remove duplicate sources from a list of strings
    Do it by creating a mapper between current themes and deduplicated themes through an LM
    """
    try:
        if "Treated" in sources:
            print("Sources already treated, skipping")
            return sources

        else:
            print("Sources not treated, running LM")

            tb = TypeBuilder()

            for source in sources:
                tb.ExistingSource.add_value(source)

            filtering_result = await b.RemoveSourcesDuplicates(sources, {"tb": tb})

            print("Sources filter reasoning: ", filtering_result.reasoning)
            print("Sources filter mapper: ", filtering_result.sources_mapper)

            final_sources = [
                filtering_result.sources_mapper[source] for source in sources
            ]

            final_sources.append("Treated")

            return final_sources

    except Exception:
        return sources
