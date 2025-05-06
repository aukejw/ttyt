import asyncio
import logging
from typing import Any

from ttyt.logging_utils import colorize
from ttyt.models.tools import execute_command

logger = logging.getLogger(__name__)


class Agent:
    """Agent that processes commands, sends them to an LLM for parsing, and executes them.

    Args:
        request_queue: Queue to get requests from
        llm_client: Client to parse natural language to shell commands
    """

    def __init__(
        self,
        request_queue: asyncio.Queue,
        llm_client: Any,
    ):
        self.request_queue = request_queue
        self.llm_client = llm_client
        self.running = False

    def run(self):
        """Main loop, processes commands from the queue and executes them."""
        logger.info("Agent started")
        self.running = True

        print("\nAgent started, try saying something!")
        while self.running:
            try:
                print("Listening.. ", end="", flush=True)
                # Blocking get from queue
                text = self.request_queue.get()
                print(f"Heard: '{colorize(text, 'LIGHT_BLUE')}'")

                # Parse the command
                command = self.llm_client.parse_command(text)
                print(f"Obtained command: '{colorize(command, 'LIGHT_BLUE')}'")

                # Execute the command, if valid and not emptystring
                if command and command != "no command":
                    logger.info(f"Executing command: {colorize(command, 'LIGHT_BLUE')}")
                    try:
                        stdout, stderr, return_code = execute_command(command)
                    except Exception as e:
                        logger.error(
                            f"Error executing command: {colorize(str(e), 'RED')}"
                        )
                        stdout, stderr, return_code = "", str(e), 1

                    # Log results
                    logger.debug(
                        f"Command: '{command}' completed with code {return_code}"
                    )

                    print(f"\n{colorize('$ ' + command, 'LIGHT_BLUE')}")
                    if stdout:
                        print(f"{colorize(stdout, 'GREEN')}")
                    if stderr:
                        print(f"{colorize(stdout, 'RED')}")

                else:
                    print()

                # Mark task as done
                self.request_queue.task_done()

            except Exception as e:
                logger.error(f"Unexpected error in processing loop: {str(e)}")

    def stop(self):
        """Stop the agent."""
        self.running = False
        self.llm_client.stop()
        logger.info("Agent stopped")
