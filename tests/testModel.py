import re
from poe_api_wrapper import AsyncPoeApi
import asyncio
import requests
from dotenv import load_dotenv
import os
import sys


# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

async def testModel(modelName, prompt):
    client = await AsyncPoeApi(tokens=tokens).create()
    finalChunk = None
    async for chunk in client.send_message(bot=modelName, message=prompt):
        finalChunk = chunk
    response = finalChunk["text"]

    print(response)

# Run the async main function
if __name__ == "__main__":
    modelName = "grok2"
    
    if len(sys.argv) > 1:
        modelName = sys.argv[1]
    
    prompt = "what model are you? (e.g. chatgpt 3.5, claude 3.7, or what?)"
    asyncio.run(testModel(modelName, prompt))