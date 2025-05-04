import logging


class TextColor:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    LIGHT_BLUE = "\033[38;5;12m"


def colorize(
    text: str,
    color_code: str,
) -> str:
    """Colorize text using ANSI escape codes."""
    color_code = getattr(TextColor, color_code.upper(), TextColor.RESET)
    return f"{color_code}{text}{TextColor.RESET}"


def configure_logger(
    logginglevel: str,
):
    """Configure the logger."""
    logging.basicConfig(
        level=logginglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
