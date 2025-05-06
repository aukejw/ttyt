import asyncio
import logging
import queue
from functools import partial

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents, Microphone

from ttyt.audio.deepgram.client import setup_deepgram_client

logger = logging.getLogger(__name__)


def on_open(self, open, **kwargs):
    logger.debug(f"Connection opened: {open}")


def on_message(self, result, request_queue, **kwargs):
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    request_queue.put(sentence)
    logger.debug(f"speaker: {sentence}")


def on_metadata(self, metadata, **kwargs):
    logger.debug(f"Metadata received: {metadata}")


def on_speech_started(self, speech_started, **kwargs):
    logger.debug(f"Speech started: {speech_started}")


def on_utterance_end(self, utterance_end, **kwargs):
    logger.debug(f"Utterance ended: {utterance_end}")


def on_error(self, error, **kwargs):
    logger.debug(f"Error occurred: {error}")


def on_close(self, close, **kwargs):
    logger.debug(f"Connection closed: {close}")


class MicrophoneListener:
    def __init__(self, request_queue: queue.Queue):
        self.request_queue = request_queue
        self.setup_dg_client()

    def setup_dg_client(self):
        deepgram: DeepgramClient = setup_deepgram_client()
        logger.info("Set up Deepgram client")

        dg_connection = deepgram.listen.websocket.v("1")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(
            LiveTranscriptionEvents.Transcript,
            partial(on_message, request_queue=self.request_queue),
        )
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        self.dg_connection = dg_connection

    def start(self):
        options: LiveOptions = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To force UtteranceEnd, the following must be true
            interim_results=False,
            # utterance_end_ms="1000",
            vad_events=True,
            keywords=[
                "pytest",
                "ls",
                "mkdir",
                "cd",
                "echo",
                "cat",
            ],
        )
        self.dg_connection.start(options)

        self.microphone = Microphone(self.dg_connection.send)
        self.microphone.start()

    def stop(self):
        self.microphone.finish()
        self.dg_connection.finish()


if __name__ == "__main__":
    # We can run the listener only, as is..
    logging.basicConfig(level=logging.DEBUG)

    # Create a request queue
    request_queue = asyncio.Queue()

    # Setup the microphone client
    listener = MicrophoneListener(request_queue)
    listener.start()

    input("Press Enter to stop...")
    listener.stop()
