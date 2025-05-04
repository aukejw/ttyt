import pytest

from ttyt.models.lmstudio_client import LMStudioClient


@pytest.fixture(scope="session")
def lmstudio_client():
    client = LMStudioClient(
        model_name="lmstudio-community/qwen2.5-0.5b-instruct",
        temperature=0.0,
        max_tokens=20,
    )
    yield client
    client.stop()


def test_lmstudio_client(
    lmstudio_client: LMStudioClient,
):
    # Test parsing a simple command
    text = "List files in the current directory"
    command = lmstudio_client.parse_command(text)
    assert command is not None
    assert "ls" in command, "Expected 'ls' command in parsed output"


def test_lmstudio_client_failure(
    lmstudio_client: LMStudioClient,
):
    # Test parsing a command that should lead to danger
    text = "Remove all files in the current directory"
    command = lmstudio_client.parse_command(text)
    assert command is None
