import openai

openai.api_key = "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"

async def transcribe(filename):
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("Recorded: \"" + transcript.text + "\"")
    return transcript.text

# transcribe('./recording.wav')
