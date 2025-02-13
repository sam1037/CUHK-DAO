# TODO rename this and refactor, this file is actually generating the image

from poe_api_wrapper import AsyncPoeApi
from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path
import time
from imgGen import generatePoemImage, saveImgFromUrl
from evalResponseParser import parseRegenerate
import json


# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

# this function is abondoned, don't use
async def getImgGenPrompt(poemObj):

    client = await AsyncPoeApi(tokens=tokens).create()

    cleanedPoemObj = {'title': poemObj['title'], 'body': '\n'.join(poemObj['body'])}

    message = f""" You are an expert in converting modern Chinese poetry into prompts for image generation. Follow these steps:
1. **Identify Key Elements**: Extract objects, scenes, and metaphors (e.g., "大海" → ocean, "春天" → cherry blossoms).
2. **Determine Style**: Suggest an artistic style (e.g., ink wash painting, surrealism, digital art).
3. **Mood & Atmosphere**: Describe emotions (e.g., hopeful, melancholic) and lighting (e.g., golden hour, dimly lit).
4. **Avoid Ambiguity**: Replace abstract phrases with concrete visuals (e.g., "寻找光明" → "a sunrise breaking through dark clouds").

**Output Format**:
- A single prompt in English (for Stable Diffusion/DALL-E) or Chinese (for ERNIE-ViLG).
- Include style, key elements, and mood.

**Example**:
- Poem: "黑夜给了我黑色的眼睛，我却用它寻找光明"
- Output: "A close-up of glowing dark eyes in a starry night, gazing at a bright sunrise over mountains, surreal digital art, vibrant colors, dramatic lighting, by James Jean and Wenqing Yan."

Now process this poem: 
Title: {cleanedPoemObj['title']}
Poem: {cleanedPoemObj['body']}
"""

    print(f"Prompt for img gen: \n{message}")

    # get response from the bot
    client = await AsyncPoeApi(tokens=tokens).create()
    finalChunk = None
    async for chunk in client.send_message(bot="Claude-3.5-Sonnet-200k", message=message):
        finalChunk = chunk
    print("-----------------")

    # return the response, ie the prompt for img gen. 
    return(finalChunk["text"])


# manually created poem obj for test
poemObj1 = {
    "title": "紙枷鎖",
    "body": ["白紙 框住了白鳥",
            "他失去 失去它的自由",
            "悉因這張強勢的紙",
            "悉因這軟弱泛黃紙",
            "他等待 等待胴體轉黃",
            "黃紙 框不住從前的白鳥"]
}

poemObj = {
    "title": "大家都是殺人犯",
    "body": [
        "彎著靈魂道謝的同時",
        "也已經學會了低聲的嘶吼",
        "哀婉而漫長的輓聲",
        "在沒有空氣的密室裡擴散開來",
        "他的嘴角和黑色的頭髮連成一氣",
        "耳朵的銳利和胸腔上的匕首圖樣吻合",
        "最後的一樁腳步是",
        "女人身旁的血泊"
    ]
}

poemObj2 = {
    "title": "秋天，金色的光芒",
    "body": [
        "她坐在窗邊吟誦唐詩",
        "時光像江河一樣",
        "在永遠不老的詩歌裡",
        "慢慢地流淌",
        "她像睿智的垂釣者",
        "一整天坐在江邊",
        "垂釣幸福和悠閒",
        "任由天空的大雁",
        "匆匆經過和飛離",
        "秋風輕輕吹拂",
        "窗簾上的楓葉",
        "一片片飄落",
        "在她自由而高潔的身軀上",
        "閃耀著金色的光芒"
    ]
}

# function to ask the LLM to analysis the poem
async def analysisPoem(poemObj):
    # setup client and get poem obj cleaned
    client = await AsyncPoeApi(tokens=tokens).create()
    cleanedPoemObj = {'title': poemObj['title'], 'body': '\n'.join(poemObj['body'])}

    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath / "analysisPoem.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format(title=cleanedPoemObj['title'], body=cleanedPoemObj['body'])
    print(f"[DEBUG] Prompt for poem analysis") # for debug

    # send msg to the bot, get response and chatID
    finalChunk = None
    async for chunk in client.send_message(bot="Claude-3.5-Sonnet-200k", message=message):
        finalChunk = chunk
    chatId = finalChunk["chatId"]
    analysis = finalChunk["text"]

    return client, chatId, analysis

# function to ask LLM to create prompt for img gen, return the prompt
async def imgGenPromptGeneration(client, chatId, analysis):
    artstlye = ""

    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"imgGenPromptGeneration.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format(artstyle = artstlye)
    print(f"\n[DEBUG] Prompt for imgGenPromptGeneration: \n{message}") # for debug

    # send msg to the bot, get the prompt for image generation
    finalChunk = None
    time.sleep(1) # this is needed to get the correct response, very stange
    async for chunk in client.send_message(bot="Claude-3.5-Sonnet-200k", message=message, chatId=chatId):
        finalChunk = chunk
    imgGenPrompt = finalChunk["text"]

    # verify if response is diff from last response
    while imgGenPrompt == analysis or imgGenPrompt == '':
        print("ERROR: img gen prompt same as analysis or empty, retrying")
        print("img gen prompt:\n", imgGenPrompt)
        time.sleep(1)
        previous_messages = await client.get_previous_messages('Claude-3.5-Sonnet-200k', chatId=chatId, count=1)
        print(previous_messages, type(previous_messages))
        imgGenPrompt = previous_messages[0]["text"]


    print("\n[DEBUG] imgGenPrompt: \n", imgGenPrompt) #debug

    return imgGenPrompt

# function to ask LLM to evaluate the generated image, return if need to regenerate
async def evaluateImg(client, chatId, imgURL):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"evaluateImg.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format(imgURL = imgURL)

    print(f"[DEBUG] Prompt for evaluating image: \n{message}") # for debug

    # send msg to the bot, get response and parse to decide if need to regenerate or not
    finalChunk = None
    async for chunk in client.send_message(bot="Claude-3.5-Sonnet-200k", message=message, chatId=chatId):
        finalChunk = chunk
    response = finalChunk["text"]
    print("[DEBUG] evaluate img response: \n", response)

    # TODO: need verify if this response is diff from last response?

    return parseRegenerate(response), response

# function to ask LLM to regenerate the prompt for img gen
async def imgGenPromptRegenerate(client, chatId, prevRespose):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"imgGenPromptRegeneration.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format()
    print(f"\n[DEBUG] Prompt for imgGenPromptRegeneration: \n{message}") # for debug

    # send msg to the bot, get the prompt for image generation
    finalChunk = None
    time.sleep(1) # this is needed to get the correct response, very stange

    async for chunk in client.send_message(bot="Claude-3.5-Sonnet-200k", message=message, chatId=chatId):
        finalChunk = chunk
    imgGenPrompt = finalChunk["text"]

    while imgGenPrompt == prevRespose or imgGenPrompt == '':
        print("ERROR: img gen prompt same as prev. response or empty, retrying")
        print("img gen prompt:\n", imgGenPrompt)
        time.sleep(1)
        previous_messages = await client.get_previous_messages('Claude-3.5-Sonnet-200k', chatId=chatId, count=1)
        print(previous_messages, type(previous_messages))
        imgGenPrompt = previous_messages[0]["text"]


    print("\n[DEBUG] imgGenPrompt: \n", imgGenPrompt) #debug

    return imgGenPrompt


async def generateAndSaveImg(poemObj):
    # analysis poem, get prompt, generate image
    client, chatId, analysis = await analysisPoem(poemObj)
    imgGenPrompt = await imgGenPromptGeneration(client, chatId, analysis)
    imgURL = await generatePoemImage(imgGenPrompt)
    print("[DEBUG] url\n", imgURL)
    needRegenerate, evalResponse = await evaluateImg(client, chatId, imgURL)
    print(f"[DEBUG] need regenerate: {needRegenerate}")

    # regenerate based on the evaluation until its good or the limit is reached
    regenLimit = 2
    regenCount = 0
    prevResponse = evalResponse
    while needRegenerate and regenCount < regenLimit:
        regenCount += 1

        print(f"[DEBUG] Regenerating image: {regenCount}-th try")
        imgGenPrompt = await imgGenPromptRegenerate(client, chatId, prevResponse)
        print("[DEBUG] Regenerated img gen prompt")

        imgURL = await generatePoemImage(imgGenPrompt)
        print("[DEBUG] new url\n", imgURL)

        needRegenerate, evalResponse = await evaluateImg(client, chatId, imgURL)
        prevResponse = evalResponse #?
        print(f"[DEBUG] need regenerate: {needRegenerate}")
        
        
    # save the resulting image
    print("[DEBUG] final image url\n", imgURL)
    saveImgFromUrl(imgURL, f"generatedImages\\testingImages\\{poemObj['title']}.png")
    
# get a poemObj given its name and issueNumber
def loadOnePoem(poemName, issueNum):
    templatePath = Path(__file__).parent.parent.parent / "data" / f"issueNumber{issueNum}"
    file_to_open = templatePath / f"{poemName}.json"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        poemObj = json.load(f)
    return poemObj


async def test():
    # get the poem obj
    poemObj = loadOnePoem("河與樹", 12)
    print(poemObj)

    # generate and save img for the given poem
    await generateAndSaveImg(poemObj)


if __name__ == "__main__":
    asyncio.run(test())