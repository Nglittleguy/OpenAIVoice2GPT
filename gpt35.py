import sys
import json
import openai
from secretKeys import OPEN_AI_KEY
openai.api_key = OPEN_AI_KEY

SYSTEM_SET = {
    "role": "system",
    "content": "You are a helpful assistant.",
}


def generatePrompt(prompt):
    return """{}""".format(prompt)


def generateMessages(prompt, logContext):
    messages = [SYSTEM_SET]
    
    with open('conversation-log.json', 'r') as log:
        global context
        context = json.load(log)

    limitedContext = context[-logContext:]

    for line in limitedContext:
        messages.append(line)

    requestMsg = {"role": "user", "content": generatePrompt(prompt)}

    messages.append(requestMsg)
    context.append(requestMsg)
    print(messages)

    return messages


def request(prompt, logContext):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generateMessages(prompt, logContext)
    )
    print("ChatGPT:\n*********************\n" + response['choices'][0]['message']['content'] + "\n*********************\n")
    responseMsg = {"role": "assistant", "content": response['choices'][0]['message']['content']}
    context.append(responseMsg)
    with open("conversation-log.json", "w") as log:
        json.dump(context, log)

# request(sys.argv[1])
