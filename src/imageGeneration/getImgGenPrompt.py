from poe_api_wrapper import AsyncPoeApi
from dotenv import load_dotenv
import os

# get poe api wrapper token
load_dotenv()
tokens = {
    'p-b': os.getenv('p-b'),
    'p-lat': os.getenv('p-lat')
}

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
    async for chunk in client.send_message(bot="gpt3_5", message=message):
        finalChunk = chunk
    print("-----------------")

    # return the response, ie the prompt for img gen. 
    return(finalChunk["text"])