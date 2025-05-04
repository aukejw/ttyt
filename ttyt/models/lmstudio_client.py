import logging
from typing import Optional

import lmstudio as lms

from ttyt.models.command_parsing import validate_command

logger = logging.getLogger(__name__)


class LMStudioClient:
    """Client for LM Studio models that parses natural language into shell commands.

    Args:
        host: The host URL where LM Studio is running
        model_name: Name of the model to use in LM Studio
        temperature: Sampling temperature (lower = more deterministic)
        max_tokens: Maximum number of tokens to generate

    """

    def __init__(
        self,
        host: str = "http://localhost:1234/v1",
        model_name: str = "lmstudio-community/gemma-3-4B-it-qat-GGUF",
        temperature: float = 0.1,
        max_tokens: int = 256,
    ):
        self.host = host
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize LM Studio client (here using convenience API, to keep client alive)
        self.model = lms.llm(model_name)
        self.setup_chat()

        logger.info(f"LM Studio client initialized with model {model_name} at {host}")

    def stop(self):
        self.model.unload()

    def setup_chat(self):
        system_prompt = (
            "You are a voice command interpreter that converts natural language requests into bash commands. "
            "If you cannot determine a bash command, respond with 'no command'. "
            "If you can determine a bash command, make sure the command is precise and covers each part of the request. "
            "Do not just repeat the input with 'echo' in front of it. "
            "Prioritize safety - never generate destructive commands like deleting files unless explicitly requested."
            "Respond with ONLY the corresponding shell command, nothing else. "
        )
        self.chat = lms.Chat(system_prompt)

    def parse_command(self, text: str) -> Optional[str]:
        """
        Parse natural language into a shell command using LM Studio.

        Args:
            text: Natural language text to parse

        Returns:
            Shell command string or None if parsing failed

        """
        try:
            # Create system and user prompts
            user_prompt = (
                f"Try to convert this request into an executable bash command: '{text}'"
            )
            self.chat.add_user_message(user_prompt)

            response = self.model.respond(
                self.chat,
                config=dict(
                    temperature=self.temperature,
                    maxTokens=self.max_tokens,
                ),
            )

            # Extract the command from the response
            command = response.content.strip()
            logger.info(f"Request: '{text}'")
            logger.info(f"Command: '{command}'")
            self.chat.add_assistant_response(command)

            # Simple validation
            if response.stats.stop_reason != "eosFound":
                raise ValueError(
                    f"Response did not end with EOS token, so the command "
                    f"'{command}' must be incomplete."
                )
            validate_command(command)
            return command

        except Exception as e:
            logger.error(f"Error parsing command: {str(e)}")
            return None
