import re

class RegenerateParseError(Exception):
    """Custom exception for regenerate parsing errors"""
    pass

def parseRegenerate(text):
    # Check for empty or None input
    if not text:
        raise RegenerateParseError("Input text cannot be empty or None")
    
    # Split text into lines and filter out truly non-empty lines after stripping
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        raise RegenerateParseError("No non-empty lines found in input")
    
    # Pattern to match various formats of the regenerate directive
    # This covers:
    # - Regenerate: YES/NO
    # - Regenerate: **YES/NO**
    # - **Regenerate: YES/NO**
    pattern = re.compile(r'(?:\*\*)?\s*Regenerate:\s*(?:\*\*)?\s*(\*\*)?([A-Za-z]+)(?:\*\*)?', re.IGNORECASE)
    
    # Search all lines
    for line in lines:
        match = pattern.search(line)
        if match:
            # Extract the value (group 2 is the actual YES/NO value)
            value = match.group(2).upper().strip()
            
            # Validate the value
            if value in ['YES', 'NO']:
                return value == 'YES'
            else:
                raise RegenerateParseError(f"Value after 'Regenerate:' must be 'YES' or 'NO', got '{value}'")
    
    # If no valid "Regenerate:" line is found, raise an error
    raise RegenerateParseError("No valid 'Regenerate:' line found in the input")

# clean up response from reasoning llm (the thinking part)
def cleanReasoningLLMResponse(text):
    """
    Removes the thinking part from text that starts with variations of 'Thinking...'
    and ends before the actual response.
    
    Args:
        text (str): Input text containing thinking and actual response parts
        
    Returns:
        str: Cleaned text with only the actual response
    """
    # Check if the text is empty
    if not text:
        return ""
        
    # Split the text by lines
    lines = text.strip().split('\n')
    
    thinking_started = False
    blank_line_after_thinking = False
    actual_response_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        # Check for various "thinking" indicators
        stripped_line = line.strip().lower()
        
        # Handle various formats with more flexibility for spaces and formatting
        if ("thinking..." in stripped_line or "thinking ..." in stripped_line):
            # Remove common markdown formatting characters
            clean_line = stripped_line.replace('*', '').replace('_', '').replace('`', '').strip()
            if clean_line.startswith("thinking"):
                thinking_started = True
                i += 1
                # Check if next line is blank
                if i < len(lines) and not lines[i].strip():
                    blank_line_after_thinking = True
                    i += 1
                continue
        
        if thinking_started:
            # If line starts with '>', it's still part of thinking
            if line.strip().startswith('>'):
                i += 1
                continue
            # Otherwise, we've reached the actual response
            else:
                thinking_started = False
                # Skip any blank line that might be after the thinking section
                if blank_line_after_thinking and not line.strip():
                    i += 1
                    blank_line_after_thinking = False
                    continue
        
        # If we're not in the thinking section, add the line to our result
        if not thinking_started:
            # Skip empty lines at the very beginning of the response
            if line.strip() or actual_response_lines:
                actual_response_lines.append(line)
        i += 1
    
    return '\n'.join(actual_response_lines).strip()


def test():
    # Example tests (commented out)
    # Test examples
    test_strings = [
        # Valid cases
        '''Regenerate: NO''',
        '''Regenerate: **NO**''',
        
        '''Some intro text.
    Regenerate: YES
    Additional text.''',
        
        '''**Regenerate: YES**''',
        
        '''Some text
    **Regenerate: NO**
    Extra text''',
        
        # Error cases
        '',  # empty string
        'Wrong format',  # wrong format
        'Regenerate: MAYBE'  # invalid value
    ]

    for i, test in enumerate(test_strings):
        print(f"Test case {i+1}:")
        try:
            result = parseRegenerate(test)
            print("Result:", result, "\n")
        except RegenerateParseError as e:
            print("Error:", str(e), "\n")

def testClean():
    # Test examples
    test_strings = [
        # Standard format
        '''Thinking ...
> thinking sent 1
> thinking sent 2
> thinking sent 3

Actual response line 1
Actual response line 2
Actual response line 3''',
        
        # No space variant
        '''Thinking...
> thinking sent 1
> thinking sent 2
Actual response line 1
Actual response line 2''',
        
        # Italic variant with underscores
        '''_Thinking..._
> thinking sent 1
> thinking step 2
Here is the actual response.
More response text.''',
        
        # Bold variant with asterisks
        '''**Thinking...**
> thinking sent 1
> thinking sent 2


Actual response line 1
Actual response line 2''',
        
        # Space before formatting
        ''' *Thinking...*
> thinking sent 1
> thinking sent 2
Actual response with space before asterisks.''',
        
        # Space after formatting
        '''*Thinking...* 
> thinking sent 1
> thinking sent 2
Response after space-after-asterisk case.''',
        
        # Mixed case variant
        '''ThInKiNg...
> thinking sent 1
> thinking sent 2
Actual response here.''',
        
        # No thinking section
        '''This is just a regular response
with no thinking part.''',
        
        # Empty string
        '',
        
        # Just thinking with no response
        ''' Thinking...

> thinking sent 1
> thinking sent 2
> thinking sent 3'''
    ]

    for i, test in enumerate(test_strings):
        print(f"Test case {i+1}:")
        print("Input:")
        print(f"'''{test}'''")
        result = cleanReasoningLLMResponse(test)
        print("\nResult:")
        print(f"'''{result}'''")
        print("\n" + "-"*50 + "\n")



if __name__ == "__main__":
    testClean()
    actualExample = """ *Thinking...*

> Let me craft an image generation prompt based on the Chinese modern poem "我病了還是這個社會病了" (Am I Sick or Is Society Sick?), focusing primarily on the core message while selecting an appropriate art style. 
>
> First, let me identify the core message again:
> - The poem explores the moral dilemma between wanting to help others and fearing the consequences in a society where good deeds might be punished
> - It questions whether moral paralysis is an individual failing or a societal problem
> - There's a tension between duty and self-preservation
> - The "sickness" metaphor applies to both individual and society
>
> For the art style, I need to choose something that can convey this internal conflict and social commentary effectively. Some options:
> - Social realism - could effectively convey the urban settings and social critique
> - Surrealism - might help visualize the internal conflict and "sickness" metaphor
> - Contemporary minimalism - could highlight isolation and moral dilemmas
> - Chinese ink wash painting with modern elements - could connect traditional values with modern conflicts
>
> I think social realism with slight surrealist elements would work well, as it can show both the concrete urban scenarios while suggesting the internal conflict.
>
> Now for the prompt, focusing on the core message:
>
> A prompt that captures the core message might include:
> - A figure standing at a crossroads or intersection
> - Multiple scenes of people needing help in the background (elderly person fallen, theft occurring)      
> - The main figure looking torn or divided
> - Perhaps shadow hands reaching toward others but being held back
> - A visual representation of the "sickness" metaphor - perhaps something suggesting a societal illness   
> - Urban setting to ground it
>
> Let me craft the prompt now, keeping it under 100 words:

A person standing frozen at a busy urban intersection, their shadow extending toward three separate scenes: an elderly person fallen on the sidewalk, a theft occurring in a marketplace, and a struggle on a bus. Their expression shows internal conflict—half their face appears concerned while the other half shows fear. Around them, invisible chains or thorns restrain their reaching hands. The background shows a modern city with distorted, sickly architecture. Use social realism style with subtle surrealist elements, muted colors except for red highlighting moral choices, conveying the paralyzing tension between moral duty and self-preservation in a distrustful society."""

    print(cleanReasoningLLMResponse(actualExample))