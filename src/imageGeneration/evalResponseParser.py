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


if __name__ == "__main__":
    test()