import os
import shutil

import dotenv
import fire

from ttyt import REPO_ROOT


def main():
    dotenv_path = REPO_ROOT / ".env"

    if dotenv_path.exists():
        print(
            f"Env file already exists at {dotenv_path}. "
            f"If you want to reinitialize it, please delete it first."
        )

    else:
        shutil.copy(REPO_ROOT / ".env.template", REPO_ROOT / ".env")
        deepgram_api_key = input(
            "Enter your Deepgram API key (https://console.deepgram.com): "
        )

        # write the `API key to the env file
        with (REPO_ROOT / ".env.template").open("r") as f:
            lines = f.readlines()

        for line_index, line in list(enumerate(lines)):
            if line.startswith("DEEPGRAM_API_KEY="):
                lines[line_index] = f"DEEPGRAM_API_KEY={deepgram_api_key}\n"

        with open(REPO_ROOT / ".env", "w") as f:
            f.writelines(lines)

        print("Env file initialized.")

    # Show contents
    dotenv.load_dotenv()

    for key in [
        "DEEPGRAM_API_KEY",
        "SYSTEM_PROMPT",
        "USER_PROMPT_PREFIX",
    ]:
        print(f"  {key:<30} = {os.environ[key]}")


if __name__ == "__main__":
    fire.Fire(main)
