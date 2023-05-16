# OpenAIVoice2GPT
This is a program to utilize OpenAI Whisper transcribe to speak to ChatGPT. 
use 'python ./voice2GPT.py'

- Add a local file of 'secretKeys.py' with 'OPEN_AI_KEY="______"'

The contextual log will be recorded in conversation-log.json.
To change the usage of the log, put an argument of n, where n is the last n messages that should be used in the generation of the new message for context
- minimum is '1', while '0' uses the entire history
- default is '5' contextual messages
