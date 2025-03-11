# 3rd party evaluator

import re
from poe_api_wrapper import AsyncPoeApi
import asyncio
from dotenv import load_dotenv
import os
from pathlib import Path
from evalResponseParser import parseRegenerate
import time

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

#TODO: why can't upload multiple files? I don't need this though

# function to ask LLM to evaluate the generated image, return if need to regenerate
async def thirdPartyEvaluateImg(client, chatId, imgURL, poemObj, analysis, model = "gemini_2_0_flash"):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"evaluateImg.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    cleanedPoemObj = {'title': poemObj['title'], 'body': '\n'.join(poemObj['body'])}
    message = template.format(imgURL = imgURL, poemTitle=cleanedPoemObj["title"], poemBody=cleanedPoemObj["body"])

    print(f"[DEBUG] Prompt for evaluating image: \n{message}") # for debug

    # send msg to the bot, get response and parse to decide if need to regenerate or not
    finalChunk = None
    async for chunk in client.send_message(bot=model, message=message):
        finalChunk = chunk
    response = finalChunk["text"]
    print("[DEBUG] evaluate img response: \n", response)
    print("[DEBUG] End of evaluate img response\n")
    thirdPartyChatId = finalChunk["chatId"]

    # TODO: need verify if this response is diff from last response?

    return parseRegenerate(response), response, thirdPartyChatId


# ask for suggestion if regeneration is needed from the 3rd party LLM, return the suggestion in str
async def regenSuggestion(client, chatId, prevResponse, model = "gemini_2_0_flash"):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"giveSuggestion.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format()

    print(f"[DEBUG] Prompt for giving suggestion for regeneration: \n{message}") # for debug

    # send msg to the bot, get response and parse to decide if need to regenerate or not
    finalChunk = None
    async for chunk in client.send_message(bot=model, message=message, chatId=chatId):
        finalChunk = chunk
    suggestion = finalChunk["text"]

    # verify if response is diff from last response
    while suggestion == prevResponse or suggestion == '':
        print("ERROR: suggestion for regeneration same as prev. response, or empty, retrying")
        print("suggestion:\n", suggestion)
        time.sleep(1)
        previous_messages = await client.get_previous_messages(model, chatId=chatId, count=1)
        print(previous_messages, type(previous_messages))
        suggestion = previous_messages[0]["text"]

    return suggestion