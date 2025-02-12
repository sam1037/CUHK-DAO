import re
from poe_api_wrapper import AsyncPoeApi
import asyncio
import requests
from dotenv import load_dotenv
import os

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

def extract_url(markdown_text):
    # Pattern matches URLs after ]: in the markdown
    pattern = r'\]: (https://[^\s]+)'
    urls = re.findall(pattern, markdown_text)[0]
    return urls

def saveImgFromUrl(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

# return the url of the generated image
async def generatePoemImage(prompt):
    print("DEBUG: generating image")
    # get img gen prompt
    message = prompt

    # generate image from prompt
    client = await AsyncPoeApi(tokens=tokens).create()
    finalChunk = None
    async for chunk in client.send_message(bot="playgroundv3", message=message):
        finalChunk = chunk
    print("DEBUG: generated image")
    #return url of the generated image
    url = extract_url(finalChunk["text"])
    return url


    # save the image
    # saveImgFromUrl(extract_urls(finalChunk["text"]), f"{filename}.jpg")

        
