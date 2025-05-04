# 🗣🖥️ Talk To Your Terminal 

Skilled developers build muscle memory and navigate the terminal effortlessly, instantly recalling commands 
and aliases. But what if we could make things.. a lot less precise?

Introducing Talk To Your Terminal - a new, wildly unpredictable way to interact with your computer. 
Using your voice, you can finally express joy and frustration at your terminal in a natural manner.

## Getting started

### Dependencies

You'll need:

 - [PortAudio](https://files.portaudio.com/download.html) for (cross-platform) audio playback, also available as [Homebrew](https://formulae.brew.sh/formula/portaudio).
 - [`pyenv`](https://github.com/pyenv/pyenv) to manage the python version
 - [`poetry`](https://python-poetry.org/) for dependency management

### Installation

1. Create a venv:
 
   ```
   make create-venv
   ```

2. Run the tests:
   ``` 
   make test
   ```

3. Run the agent:
   ```
   make run 
   ```

4. Talk to your terminal! Don't worry, we try to safeguard against some destructive commands.
