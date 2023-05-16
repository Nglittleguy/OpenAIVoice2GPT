from audio import record
from gpt35 import request
from whisper import transcribe
import asyncio
import sys

async def voice2GPT(context):
    
    recordingFileName = "./recording.wav"
    await record(recordingFileName)

    prompt = await transcribe(recordingFileName)
    request(prompt, context)

def main():
    contextArg = 3
    if (len(sys.argv) > 1 and sys.argv[1] and sys.argv[1].isdigit()):
        contextArg = int(sys.argv[1]) 
    asyncio.run(voice2GPT(contextArg))

main()    