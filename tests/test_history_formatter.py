import pytest

from wine_press_lm_evaluation.core.helpers.chat_history import (
    SpeakerRole,
    ChatTurn,
    convert_history_to_string,
)


@pytest.fixture
def multi_turn_history():
    """A standard history list for testing."""
    return [
        ChatTurn(SpeakerRole.USER, "What is the capital of France?"),
        ChatTurn(SpeakerRole.ASSISTANT, "The capital is Paris."),
        ChatTurn(SpeakerRole.USER, "Thank you.")
    ]

def test_empty_history_returns_empty_string():
    """Test with an empty list should return an empty string."""
    history = []
    expected = ""
    assert convert_history_to_string(history) == expected

def test_single_turn_history_no_newline():
    """Test with a single turn, ensuring no trailing newline."""
    history = [
        ChatTurn(SpeakerRole.USER, "Hello there!")
    ]
    expected = "User: Hello there!"
    assert convert_history_to_string(history) == expected

def test_multi_turn_history_correct_newlines(multi_turn_history):
    """Test with multiple turns, checking for newlines between turns, but not at the end."""
    expected = (
        "User: What is the capital of France?\n"
        "Assistant: The capital is Paris.\n"
        "User: Thank you."
    )
    assert convert_history_to_string(multi_turn_history) == expected

def test_to_string_method():
    """Test the to_string method on a single object."""
    turn = ChatTurn(SpeakerRole.ASSISTANT, "How can I help?")
    expected = "Assistant: How can I help?"
    # Note: Assuming you update ChatHistory.to_string to use .value on the Enum
    assert turn.to_string() == expected