import pytest

from ttyt.models.command_parsing import validate_command


def test_valid_commands():
    """Test that valid commands pass validation."""
    assert validate_command("ls -la") == True
    assert validate_command("echo 'hello world'") == True
    assert validate_command("git status") == True


def test_dangerous_commands():
    """Test that dangerous commands raise ValueError."""

    for command in [
        "rm -rf /",
        "sudo shutdown -h now",
        "dd if=/dev/zero of=/dev/sda",
        "mkfs.ext4 /dev/sda1",
        "reboot",
    ]:
        with pytest.raises(ValueError) as excinfo:
            validate_command("rm -rf /")
        assert "potentially dangerous" in str(excinfo.value)


def test_command_length():
    max_length_cmd = " ".join(["word"] * 20)
    assert validate_command(max_length_cmd, maxlength=20) == True

    # Create a command with one word too many
    too_long_cmd = " ".join(["word"] * 21)
    with pytest.raises(ValueError) as excinfo:
        validate_command(too_long_cmd, maxlength=20)
    assert "too long" in str(excinfo.value)


def test_edge_cases():
    assert validate_command("") == True
    assert validate_command("pwd") == True
    assert validate_command(" ".join(["x"] * 5), maxlength=5) == True

    with pytest.raises(ValueError):
        validate_command("echo 'The command rm -rf / is dangerous'")

    assert validate_command("ls -la /tmp", maxlength=5) == True
    with pytest.raises(ValueError):
        validate_command("ls -la /tmp", maxlength=2)
