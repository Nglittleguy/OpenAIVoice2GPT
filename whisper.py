import openai
from secretKeys import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY

async def transcribe(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("Recorded: \"" + transcript.text + "\"")
    return transcript.text

# transcribe('./recording.wav')
