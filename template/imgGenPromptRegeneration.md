**A third-party LLM evaluator considered the generated image not good enough, we are going to regenerate the image.**

The image url: {imgURL}

The suggestion from the third-party LLM evaluator:
"""
{suggestion}
"""

Generate a prompt that will be used to create an image of the given chinese modern verse, with consideration of the key elements, semantics and core message, focus the most on core message. Is it ok if the generated image does not capture all key elements or semantics entities, but it must convey the core message of the poem well. 

Choose an art style suitable for the poem and specify it in the prompt.

Length Requirements: maximum 100 words

The prompt should be in english only.

In the generated image, there should be no Chinese text.

**Format your response as a single, coherent prompt paragraph. No irrelevant sentences should be included. So do not respond like "Okay, the prompt for image generation is as follow: {{the actual prompt}}", instead respond "{{the actual prompt}}" directly**.