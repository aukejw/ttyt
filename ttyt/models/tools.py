import subprocess
from typing import Tuple


def execute_command(
    command: str,
    timeout: float = 10.0,
) -> Tuple[str, str, int]:
    """
    Executes a shell command synchronously.

    Args:
        command: Shell command to execute

    Returns:
        Tuple of (stdout, stderr, return_code)

    """
    # Run the command synchronously
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    # Get results
    stdout = process.stdout
    stderr = process.stderr
    return_code = process.returncode

    return stdout, stderr, return_code
