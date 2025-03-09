# this script shall generate the images for the needed poems

from getImgGenPrompt import generateAndSaveImg
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
    """Main function to run asynchronous code."""
    # custom case
    poemObj = dataLoader.loadOnePoem("我感覺到車窗的風在吹", 22)
    #poemObj = dataLoader.loadOnePoem("血玫瑰", 18)
    #poemObj = dataLoader.loadOnePoem("大家都是殺人犯", 11)
    #poemObj = dataLoader.loadOnePoem("雪老了", 38)
    await generateAndSaveImg(poemObj)  # Properly await the coroutine

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
