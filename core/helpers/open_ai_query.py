import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

from wine_press_lm_evaluation.core.helpers.chat_history import ChatTurn, SpeakerRole


async def get_gpt_answer(
    query: str, history: list[ChatTurn] = None, model: str = "gpt-5"
) -> str:
    """
    Asynchronously get an answer for a query from OpenAI's model.

    Args:
        query (str): The query to answer.
        history (list[ChatTurn]): The history of the answer.
        model (str, optional): The model to use. Defaults to "gpt-5".

    Returns:
        str: The answer to the query.
    """

    load_dotenv()

    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    history.append(ChatTurn(role=SpeakerRole.USER, content=query))

    response = await client.responses.create(
        input=query,
        model=model,
    )

    history.append(ChatTurn(role=SpeakerRole.ASSISTANT, content=response.output_text))

    return response.output_text
