# TODO rename this and refactor, this file is actually generating the image

from poe_api_wrapper import AsyncPoeApi
from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path
import time
from imgGen import generatePoemImage, saveImgFromUrl
from utils import parseRegenerate, cleanReasoningLLMResponse
import json
from imgEvaluator import thirdPartyEvaluateImg, regenSuggestion

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

# this function is abondoned, don't use
async def getImgGenPrompt(poemObj, model = "gemini_2_0_flash"):

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
    async for chunk in client.send_message(bot=model, message=message):
        finalChunk = chunk
    print("-----------------")

    # return the response, ie the prompt for img gen. 
    return(finalChunk["text"])

# function to ask the LLM to analysis the poem
async def analysisPoem(poemObj, model = "gemini_2_0_flash"):
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
    async for chunk in client.send_message(bot=model, message=message):
        finalChunk = chunk
    chatId = finalChunk["chatId"]
    analysis = finalChunk["text"]

    return client, chatId, analysis

# function to ask LLM to create prompt for img gen, clean it, then return the prompt
async def imgGenPromptGeneration(client, chatId, analysis, model = "gemini_2_0_flash"):
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
    async for chunk in client.send_message(bot=model, message=message, chatId=chatId):
        finalChunk = chunk
    imgGenPrompt = finalChunk["text"]
    chatId = finalChunk["chatId"]

    # verify if response is diff from last response
    while imgGenPrompt == analysis or imgGenPrompt == '':
        print("ERROR: img gen prompt same as analysis or empty, retrying")
        print("img gen prompt:\n", imgGenPrompt)
        time.sleep(1)
        previous_messages = await client.get_previous_messages(model, chatId=chatId, count=1)
        print(previous_messages, type(previous_messages))
        imgGenPrompt = previous_messages[0]["text"]
        chatId = previous_messages[0]["chatId"]

    print("\n[DEBUG] imgGenPrompt b4 cleaning: \n", imgGenPrompt) #debug

    # clean it (format is messy if the model is a reasoning model)
    imgGenPrompt = cleanReasoningLLMResponse(imgGenPrompt)
    print("\n[DEBUG] imgGenPrompt after cleaning: \n", imgGenPrompt) #debug

    return imgGenPrompt, chatId

# function to ask LLM to evaluate the generated image, return if need to regenerate
async def evaluateImg(client, chatId, imgURL, model = "gemini_2_0_flash"):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"evaluateImg.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format(imgURL = imgURL)

    print(f"[DEBUG] Prompt for evaluating image: \n{message}") # for debug

    # send msg to the bot, get response and parse to decide if need to regenerate or not
    finalChunk = None
    async for chunk in client.send_message(bot=model, message=message, chatId=chatId):
        finalChunk = chunk
    response = finalChunk["text"]
    print("[DEBUG] evaluate img response: \n", response)
    print("[DEBUG] End of evaluate img response\n")

    # TODO: need verify if this response is diff from last response?

    return parseRegenerate(response), response

# function to ask LLM to regenerate the prompt for img gen
async def imgGenPromptRegenerate(client, chatId, prevRespose, imgURL, suggestion, model = "gemini_2_0_flash"):
    # get message to feed to LLM
    templatePath = Path(__file__).parent.parent.parent / "template"
    file_to_open = templatePath/"imgGenPromptRegeneration.md"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        template = f.read()
    message = template.format(imgURL=imgURL, suggestion=suggestion)
    print(f"\n[DEBUG] Prompt for imgGenPromptRegeneration: \n{message}") # for debug

    # send msg to the bot, get the prompt for image generation
    finalChunk = None
    time.sleep(1) # this is needed to get the correct response, very stange

    async for chunk in client.send_message(bot=model, message=message, chatId=chatId):
        finalChunk = chunk
    imgGenPrompt = finalChunk["text"]

    while imgGenPrompt == prevRespose or imgGenPrompt == '':
        print("ERROR: img gen prompt same as prev. response or empty, retrying")
        print("img gen prompt:\n", imgGenPrompt)
        time.sleep(1)
        previous_messages = await client.get_previous_messages(model, chatId=chatId, count=1)
        print(previous_messages, type(previous_messages))
        imgGenPrompt = previous_messages[0]["text"]


    print("\n[DEBUG] imgGenPrompt: \n", imgGenPrompt) #debug

    return imgGenPrompt


#TODO enable customize the path of saved image
async def generateAndSaveImg(poemObj, model = "gemini_2_0_flash", imgModel = "playgroundv3"):
    shareCodes = {
        "firstLLM": "",
        "1stEvalLLM": "",
        "2ndEvalLLM": "",
        "3rdEvalLLM": "",
    }

    # analysis poem, get prompt, generate image, get chatIds, evaluate
    client, analysisChatId, analysis = await analysisPoem(poemObj, model)
    imgGenPrompt, imgGenPromptChatId = await imgGenPromptGeneration(client, analysisChatId, analysis, model)
    imgURL, imgGenChatId = await generatePoemImage(imgGenPrompt, imgModel)
    
    print("[DEBUG] url\n", imgURL)
    needRegenerate, evalResponse, thirdPartyChatId = await thirdPartyEvaluateImg(client, analysisChatId, imgURL, poemObj, analysis, model)
    print(f"[DEBUG] need regenerate: {needRegenerate}")

    # update chatIds or sharecode
    firstLLMShareCode = await client.share_chat(model, analysisChatId)
    evalShareCode1 = await client.share_chat(model, thirdPartyChatId)
    evalShareCode2 = ""
    evalShareCode3 = ""
    

    # regenerate based on the evaluation until its good or the limit is reached
    regenLimit = 2
    regenCount = 0
    prevResponse = evalResponse
    while needRegenerate and regenCount < regenLimit:
        regenCount += 1
        # get suggestion from 3rd party evaluator
        suggestion = await regenSuggestion(client, thirdPartyChatId, evalResponse, model)
        # update sharecode accordingly
        tempShareCode = await client.share_chat(model, thirdPartyChatId)
        if regenCount == 1:
            evalShareCode1 = tempShareCode
        elif regenCount == 2:
            evalShareCode2 = tempShareCode

        # regenerate prompt in 1st LLM and update sharecode
        print(f"[DEBUG] Regenerating image: {regenCount}-th try")
        imgGenPrompt = await imgGenPromptRegenerate(client, analysisChatId, prevResponse, imgURL, suggestion, model)
        print("[DEBUG] Regenerated img gen prompt")
        firstLLMShareCode = await client.share_chat(model, analysisChatId)
        # regenerate the image
        imgURL, imgGenChatId = await generatePoemImage(imgGenPrompt, imgModel)
        print("[DEBUG] new url\n", imgURL)
        # evaluate again
        needRegenerate, evalResponse, thirdPartyChatId = await thirdPartyEvaluateImg(client, analysisChatId, imgURL, poemObj, analysis, model)
        prevResponse = evalResponse #?
        print(f"[DEBUG] need regenerate: {needRegenerate}")
        # update shareCodes
        tempShareCode = await client.share_chat(model, thirdPartyChatId)
        if regenCount == 1:
            evalShareCode2 = tempShareCode
        elif regenCount == 2:
            evalShareCode3 = tempShareCode
            
    # save the resulting image
    print("[DEBUG] final image url\n", imgURL)
    saveImgFromUrl(imgURL, f"generatedImages\\compareTextModels\\{poemObj['title']}_{model}_{imgModel}.png")

    # save the sharecode and save as json file
    shareCodes["firstLLM"] = firstLLMShareCode
    shareCodes["1stEvalLLM"] = evalShareCode1
    shareCodes["2ndEvalLLM"] = evalShareCode2
    shareCodes["3rdEvalLLM"] = evalShareCode3
    print("[DEBUG] shareCodes: \n", shareCodes)

    issue_number = poemObj.get('issueNumber', 'unknown')
    shareCodesPath = Path(__file__).parent.parent.parent / "textModelsShareCodes"
    shareCodesPath.mkdir(parents=True, exist_ok=True)
    with open(shareCodesPath / f"{poemObj['title']}_{model}_{imgModel}.json", 'w', encoding='utf-8') as f:
        json.dump(shareCodes, f, ensure_ascii=False, indent=4)
    

# get a poemObj given its name and issueNumber
def loadOnePoem(poemName, issueNum):
    templatePath = Path(__file__).parent.parent.parent / "data" / f"issueNumber{issueNum}"
    file_to_open = templatePath / f"{poemName}.json"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        poemObj = json.load(f)
    return poemObj


async def test():
    # get the poem obj
    #poemObj = loadOnePoem("偽童話", 45)
    #poemObj = loadOnePoem("劊子手的長嘆", 15)
    #poemObj = loadOnePoem("住在精神病院隔壁", 12)
    poemObj = loadOnePoem("大家都是殺人犯", 11) # this one will probably regenerate
    
    print(poemObj)

    # generate and save img for the given poem
    await generateAndSaveImg(poemObj)


if __name__ == "__main__":
    asyncio.run(test())