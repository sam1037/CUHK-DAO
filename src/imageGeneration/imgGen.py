import re
from poe_api_wrapper import AsyncPoeApi
import asyncio
import requests
from dotenv import load_dotenv
import os
from .getImgGenPrompt import getImgGenPrompt 

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

def extract_urls(markdown_text):
    # Pattern matches URLs after ]: in the markdown
    pattern = r'\]: (https://[^\s]+)'
    urls = re.findall(pattern, markdown_text)[0]
    return urls

def saveImgFromUrl(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

async def generatePoemImage(poemObj, filename):
    # get img gen prompt
    message = await getImgGenPrompt(poemObj)
    print(f"Prompt for img gen: \n{message}")

    # generate image from prompt
    client = await AsyncPoeApi(tokens=tokens).create()
    finalChunk = None
    async for chunk in client.send_message(bot="playgroundv3", message=message):
        finalChunk = chunk
    print("-----------------")
    print(finalChunk["text"])
    
    # save the image
    saveImgFromUrl(extract_urls(finalChunk["text"]), f"{filename}.jpg")

        
