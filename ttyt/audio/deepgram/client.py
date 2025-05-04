import os

from deepgram import DeepgramClient, DeepgramClientOptions
from deepgram.utils import verboselogs
from dotenv import load_dotenv


def setup_deepgram_client(verbose=False, **options) -> DeepgramClient:
    """Set up the client."""
    config: DeepgramClientOptions = DeepgramClientOptions(
        options={
            "keepalive": "true",
            "microphone_record": "true",
            "speaker_playback": "true",
            **options,
        },
        verbose=verboselogs.DEBUG if verbose else verboselogs.WARNING,
    )

    # Get the API key from the env file
    load_dotenv()
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    deepgram: DeepgramClient = DeepgramClient(
        api_key=deepgram_api_key,
        config=config,
    )

    return deepgram
