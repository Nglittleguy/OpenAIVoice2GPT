import sys
import json
import openai
from textData import importText, getCustomerInfo
from secretKeys import OPEN_AI_KEY
openai.api_key = OPEN_AI_KEY

SYSTEM_SET = {
    "role": "system",
    "content": "You are a travel guide assisting the user.",
}

cName = "DEMO NAME"
cTitle = "Mrs"
cHotel = 0
cId = 0


def hotelInfo(customerHotel):
    return {
        "role": "system",
        "content": "Use the following the answer the queries: {}".format(importText(customerHotel))
    }


def greetUser(customerName, customerTitle):
    return {
        "role": "system",
        "content": "Preface the answer by greeting the user as {}.{}".format(customerTitle, customerName)
    }

# KIOSK ROLE
# "content": "You are a travel guide assisting the user.",
# "role": "system",
# "content": "Use the following the answer the queries: {}".format(importText(1))

# ASSISTANT ROLE
# "content": "You are a helpful assistant.",


def generatePrompt(prompt):
    return """{}""".format(prompt)


def generateMessages(prompt, logContext):
    global cName, cTitle, cHotel, cId

    messages = [SYSTEM_SET]
    cId = sys.argv[2]
    customerData = getCustomerInfo(cId)

    try:
        cName = customerData[1]
        cTitle = customerData[2]
        cHotel = customerData[3]
        messages.append(hotelInfo(cHotel))
    except:
        return 0

    # Comment out if no context
    try:
        with open('./conversations/{}.json'.format(cId), 'r') as log:
            global context
            context = json.load(log)

        limitedContext = context[-logContext:]

        for line in limitedContext:
            messages.append(line)

    except FileNotFoundError:
        context = []
        messages.append(greetUser(cName, cTitle))

    requestMsg = {"role": "user", "content": generatePrompt(prompt)}
    messages.append(requestMsg)
    context.append(requestMsg)

    return messages


def request(prompt, logContext):
    global cId

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generateMessages(prompt, logContext)
    )
    print("ChatGPT:\n*********************\n" +
          response['choices'][0]['message']['content'] + "\n*********************\n")

    responseMsg = {"role": "assistant",
                   "content": response['choices'][0]['message']['content']}
    context.append(responseMsg)
    with open("./conversations/{}.json".format(cId), "w") as log:
        json.dump(context, log)


# Default voice assistant: 'python gpt35.py "Insert question here" CustomerID'
request(sys.argv[1], 5)
