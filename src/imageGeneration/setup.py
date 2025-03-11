# this script shall generate the images for the needed poems

from imageGeneration.generateAndSaveImg import generateAndSaveImg
import sys
import os
import asyncio

# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import the file
import dataLoader

async def main():
    #model = "o3-mini-high"
    model = "deepseekr1fw"
    #model = "deepseekr1fw"

    imgModel = "playgroundv3"
    #imgModel = "playgroundv3"
    #imgModel = "playgroundv3"

    # custom case
    #poemObj = dataLoader.loadOnePoem("我感覺到車窗的風在吹", 22)
    #poemObj = dataLoader.loadOnePoem("血玫瑰", 18) # slight mental one
    poemObj = dataLoader.loadOnePoem("大家都是殺人犯", 11) #a mental one
    #poemObj = dataLoader.loadOnePoem("住在精神病院隔壁", 12) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("腐爛或發酵", 27) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("在精神科診室", 28) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("解剖室", 36) #a mental one as well
    #poemObj = dataLoader.loadOnePoem("肉紅色燈光", 43) #a sexual one?
    #poemObj = dataLoader.loadOnePoem("陽痿病人", 43) #a sexual one?
    #poemObj = dataLoader.loadOnePoem("雪老了", 38)
    #poemObj = dataLoader.loadOnePoem("偽童話", 45)
    #poemObj = dataLoader.loadOnePoem("我病了還是這個社會病了", 34)
    #poemObj = dataLoader.loadOnePoem("敏感神經", 28) #hard to understand
    #poemObj = dataLoader.loadOnePoem("劊子手的長嘆", 15) #hard to understand
    await generateAndSaveImg(poemObj, model = model, imgModel=imgModel)  # Properly await the coroutine

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
