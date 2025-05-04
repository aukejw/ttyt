def validate_command(
    command: str,
    maxlength: int = 20,
) -> bool:
    """
    Validate that the incoming text is a shell command we can safely execute.

    Raises ValueError if the command is potentially dangerous or too complex.

    Args:
        command: The command string to validate
        maxlength: Maximum number of elements in the command, to avoid complex commands

    """
    # Basic validation: check for dangerous commands
    danger_zone = [
        "rm",
        "dd",
        "mkfs",
        "shutdown",
        "reboot",
        "sudo",
    ]
    for cmd in danger_zone:
        if cmd in command:
            raise ValueError(
                f"Command '{command}' is potentially dangerous and will not be executed."
            )

    # Further validation can be added here (e.g., regex checks)
    if len(command.split()) > maxlength:
        raise ValueError(f"Command '{command}' is too long and may be free text.")

    return True
