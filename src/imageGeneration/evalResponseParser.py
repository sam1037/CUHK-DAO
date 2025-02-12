class RegenerateParseError(Exception):
    """Custom exception for regenerate parsing errors"""
    pass

def parseRegenerate(text):
    # Check for empty or None input
    if not text:
        raise RegenerateParseError("Input text cannot be empty or None")
    
    # Get last line only
    last_line = text.split('\n')[-1].strip()
    
    # Check format
    if not last_line.startswith('Regenerate:'):
        raise RegenerateParseError("First line must start with 'Regenerate:'")
    
    # Extract and validate value
    value = last_line.replace('Regenerate:', '').strip().upper()
    if value not in ['YES', 'NO']:
        raise RegenerateParseError("Value after 'Regenerate:' must be 'YES' or 'NO'")
    
    return value == 'YES'



"""
# Test examples
test_strings = [
    # Valid cases
    '''Regenerate: NO
    The image effectively captures...''',
    
    '''Regenerate: YES
    Some immediate content without empty line''',
    
    # Error cases
    '',  # empty string
    'Wrong format',  # wrong format
    'Regenerate: MAYBE'  # invalid value
]


for test in test_strings:
    try:
        result = parse_regenerate(test)
        print("Input first line:", repr(test.split('\n')[0]))
        print("Result:", result, "\n")
    except RegenerateParseError as e:
        print("Error for input", repr(test.split('\n')[0]))
        print("Error message:", str(e), "\n")

"""