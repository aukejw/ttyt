# 🗣🖥️ Talk To Your Terminal 

[![tests-Mac](https://github.com/aukejw/ttyt/actions/workflows/tests-mac.yaml/badge.svg)](https://github.com/aukejw/ttyt/actions/workflows/tests-mac.yaml)

Skilled developers build muscle memory and navigate the terminal effortlessly, instantly recalling commands and aliases. But what if we could make things.. a lot less precise?

Introducing Talk To Your Terminal - a new, wildly unpredictable way to interact with your computer. Using your voice, you can finally express joy and frustration at your terminal in a natural manner.

## Getting started

### Dependencies

You'll need:

 - A [DeepGram](https://console.deepgram.com/signup) API key for speech-to-text. Deepgram provides 200 USD of free credits, which is enough for many hours of work.
 - [PortAudio](https://files.portaudio.com/download.html) for (cross-platform) audio playback, also available as [Homebrew](https://formulae.brew.sh/formula/portaudio).
 - [`pyenv`](https://github.com/pyenv/pyenv) to manage the python version.
 - [`poetry`](https://python-poetry.org/) for dependency management.

### Installation

1. Create a venv, and run setup to enter your Deepgram API key:
 
   ```
   make create-venv
   make init
   ```

2. Run the tests:
   ``` 
   make test
   ```

3. Run the agent:
   ```
   make run 
   ```

4. Talk to your terminal! 
   We try to safeguard against some destructive commands (e.g. deleting files).


## About this project

The goal of this project is to learn about voice-based computer use with local (small) models, and see how far current speech models are in this domain. 

Although this is not a serious contender in the race for computer use agents, there are some genuine use cases for voice-control:

  - Voice provides a communication channel that does not interfere with keyboard and mouse usage. You can simultaneously talk and type.
  - If you are completely unfamiliar with shell or bash, a natural language interface can show you the commands to run. Of course, you could just use the keyboard here.
  - If you have a visual impairment, audio becomes the main way to read the screen. There are much better ways to use audio, such as the excellent [NVDA](https://www.nvaccess.org/) screen reader.
