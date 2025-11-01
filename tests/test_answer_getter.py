from unittest.mock import patch

from openai.resources.responses import Responses

from wine_press_lm_evaluation.core.helpers.open_ai_query import get_gpt_answer


def test_get_gpt_answer():
    test_input = "Hello world"
    test_model = "gpt-19"

    with patch.object(
        target=Responses,
        attribute="create",
    ) as mock_api_call:
        get_gpt_answer(
            query=test_input,
            model=test_model,
            history=[],
        )

    assert mock_api_call.call_count == 1, "GPT API should have been called once"

    call_kwargs = mock_api_call.call_args.kwargs

    assert call_kwargs["input"] == test_input, "Query should be the correct one"
    assert call_kwargs["model"] == test_model, "Model should be the correct one"
