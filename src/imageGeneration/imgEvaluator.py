import re
from poe_api_wrapper import AsyncPoeApi
import asyncio
from dotenv import load_dotenv
import os

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

#TODO: why can't upload multiple files? I don't need this though

async def imgEvaluator():
    client = await AsyncPoeApi(tokens=tokens).create()
    filePaths = ["/home/sam1037/wslProgramming/server-bot-quick-start/poeAPIWrapper/car2.png"]
    message = f"Describe the attached images, rate how realistic each one is from 0 to 1 (higher is better)"

    # get response from the bot
    client = await AsyncPoeApi(tokens=tokens).create()
    finalChunk = None
    async for chunk in client.send_message(bot="gpt3_5", message=message, file_path=filePaths):
        finalChunk = chunk
    print("-----------------")
    print(finalChunk["text"])
    
    # rcalculate the score (higher is better)
    return 0.5

asyncio.run(imgEvaluator())