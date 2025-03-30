# this script shall generate the images for the needed poems

from generateAndSaveImg import generateAndSaveImg
import sys
import os
import asyncio
import time

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import the file
import dataLoader

async def main():
    #model = "o3-mini-high"
    #model = "Claude-3.7-Sonnet-Reasoning"
    #model = "deepseekr1fw"
    #model = "gpt4_o"
    model = "gemini_2_0_flash"

    playground = "playgroundv3"
    imagen3 = "imagen3"
    flux = "flux-pro-1.1"
    #imgModel = "imagen3-fast"
    #imgModel = "recraft-v3" # not good, can't do styling
    #imgModel = "ideogram-v2" # not good, can't do styling
    #imgModel = "ideogram-v2a" # not good, can't do styling
    
    imgModels = ["playgroundv3", "imagen3", "flux-pro-1.1"]

    o3 = "o3-mini-high"
    gpt4o = "gpt4_o"
    claude3_7 = "Claude-3.7-Sonnet"
    deepseekr1fw = "deepseekr1fw"
    genmini = "gemini_2_0_flash"

    # custom case
    #poemObj = dataLoader.loadOnePoem("我感覺到車窗的風在吹", 22)
    #poemObj = dataLoader.loadOnePoem("寧靜", 5)
    #poemObj = dataLoader.loadOnePoem("已讀不回", 15)
    #poemObj = dataLoader.loadOnePoem("午夜藍", 16)
    #poemObj = dataLoader.loadOnePoem("殤愛", 16)
    #poemObj = dataLoader.loadOnePoem("我希望我是一隻雞蛋", 20)
    #poemObj = dataLoader.loadOnePoem("血玫瑰", 18) # slight mental one
    poemObj1 = dataLoader.loadOnePoem("大家都是殺人犯", 11) #a mental one
    poemObj2 = dataLoader.loadOnePoem("住在精神病院隔壁", 12) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("腐爛或發酵", 27) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("在精神科診室", 28) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("解剖室", 36) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("肉紅色燈光", 43) #a sexual one?
    #poemObj = dataLoader.loadOnePoem("陽痿病人", 43) #a sexual one?
    #poemObj = dataLoader.loadOnePoem("雪老了", 38)
    #poemObj = dataLoader.loadOnePoem("偽童話", 45)
    poemObj3 = dataLoader.loadOnePoem("我病了還是這個社會病了", 34)
    #poemObj = dataLoader.loadOnePoem("敏感神經", 28) #hard to understand
    #poemObj = dataLoader.loadOnePoem("劊子手的長嘆", 15) #hard to understand

    # generate for all img models for one poem
    #await generateAndSaveImg(poemObj, model = model, imgModel=playground)
    #await generateAndSaveImg(poemObj, model = model, imgModel=flux)
    #await generateAndSaveImg(poemObj, model = model, imgModel=imagen3)

    # compare text models
    for poemObj in [poemObj3]:
        await generateAndSaveImg(poemObj, model = o3, imgModel=flux)
        time.sleep(5)
        await generateAndSaveImg(poemObj, model = gpt4o, imgModel=flux)
        time.sleep(5)
        await generateAndSaveImg(poemObj, model = claude3_7, imgModel=flux)
        time.sleep(5)
        await generateAndSaveImg(poemObj, model = deepseekr1fw, imgModel=flux)
        time.sleep(5)
        await generateAndSaveImg(poemObj, model = genmini, imgModel=flux)
        time.sleep(5)

    #for imgModel in imgModels:
    #    await generateAndSaveImg(poemObj, model = model, imgModel=imgModel)  # Properly await the coroutine

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
