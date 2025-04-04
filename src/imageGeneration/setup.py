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

async def generateForOneIssue(issueNum, textModel, imgMode):
    print(f"Generating images for issue {issueNum} using {textModel} and {imgMode}.")

    # load the poems for issue 1 and generate the images
    poems = dataLoader.loadOneIssue(issueNum)
    print(f"Loaded {len(poems)} poems.")
    for poem in poems:
        poemName = poem["title"]
        issueNum = poem["issueNumber"]
        # check if the poem has been generated
        if os.path.exists(f"generatedImages/actual/issueNumber{issueNum}/{poemName}_{textModel}_{imgMode}.png"):
            print(f"Image for {poemName} in issue {issueNum} already exist.")
            continue
        
        # Generate images for the poem using different models
        print(f"Generating image for {poemName} in issue {issueNum}.")
        await generateAndSaveImg(poem, textModel, imgMode)
        time.sleep(1)

async def main():
    gpt4o = "gpt4_o"
    flux = "flux-pro-1.1"

    # load the poems for a particular issue and generate the images
    issues = [10,11,12]
    for issueNum in issues:
        await generateForOneIssue(issueNum, gpt4o, flux)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
