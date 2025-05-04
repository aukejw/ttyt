import logging
import queue
import signal
import sys
from typing import Optional

import fire

from ttyt.agent.agent import Agent
from ttyt.audio.deepgram.microphone_listener import MicrophoneListener
from ttyt.logging_utils import configure_logger
from ttyt.models.lmstudio_client import LMStudioClient

# Configure logging
logger = logging.getLogger(__name__)

# Global variables for cleanup
listener: Optional[MicrophoneListener] = None
agent: Optional[Agent] = None
running = True


def shutdown(signum=None, frame=None):
    """Gracefully shut down all objects."""
    global running
    logger.info("Shutting down...")

    running = False

    # Stop the agent
    if agent:
        agent.stop()

    # Stop the microphone listener
    if listener:
        listener.stop()

    logger.info("Shutdown complete")
    sys.exit(0)


def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)


def main(
    logginglevel: str = "WARNING",
):
    """Main entry point for the application."""
    global listener, agent

    configure_logger(logginglevel=logginglevel)

    try:
        # Set up signal handling
        setup_signal_handlers()

        # Create shared queue for communication
        request_queue = queue.Queue()

        # Initialize LLM client, agent
        llm_client = LMStudioClient(
            model_name="lmstudio-community/gemma-3-4B-it-qat-GGUF",
        )
        agent = Agent(
            request_queue=request_queue,
            llm_client=llm_client,
        )

        # Initialize and start microphone listener
        listener = MicrophoneListener(request_queue)
        listener.start()

        # Start the agent (this is the main loop)
        agent.run()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        shutdown()


if __name__ == "__main__":
    fire.Fire(main)
