import os
import json
from pathlib import Path
from typing import List, Dict, Any

# Function to load poems for one issue (your existing function)
def loadOneIssue(issueNum):
    templatePath = Path(__file__).parent.parent / "data" / f"issueNumber{issueNum}"
    allPoems = []
    for file in os.listdir(templatePath):
        if file.endswith(".json"):
            with open(templatePath / file, 'r', encoding='utf-8') as f:
                poemObj = json.load(f)
                allPoems.append(poemObj)
    return allPoems

def read_template():
    """
    Read the HTML template from a file
    
    Returns:
        The HTML template as a string
    """
    template_path = Path(__file__).parent / "gallery_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_gallery_html(issue_number: int, poems: List[Dict[str, Any]], template: str) -> str:
    """
    Generate the HTML content for a specific issue
    
    Args:
        issue_number: The issue number
        poems: List of poem dictionaries for this issue
        template: HTML template
        
    Returns:
        HTML content as a string
    """
    # Convert the poems list to a JSON string that can be embedded in JavaScript
    poems_json = json.dumps(poems, ensure_ascii=False, indent=4)
    
    # Format the HTML template with the issue-specific data
    return template.format(
        issue_number=issue_number,
        poem_data_json=poems_json
    )

def generate_all_galleries(total_issues: int) -> None:
    """
    Generate all gallery HTML files
    
    Args:
        total_issues: Total number of issues to generate
    """
    # Define the output directory
    output_dir = Path(__file__).parent / "gallery_output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Read the HTML template
    template = read_template()
    
    # Generate a file for each issue
    for issue_number in range(1, total_issues + 1):
        try:
            # Load poems for this issue using your existing function
            poems = loadOneIssue(issue_number)
            
            # Generate the HTML content
            html_content = generate_gallery_html(issue_number, poems, template)
            
            # Write to file
            output_path = output_dir / f"poetry-gallery-issue-{issue_number}.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"Generated gallery for Issue {issue_number} with {len(poems)} poems")
            
        except Exception as e:
            print(f"Error generating gallery for Issue {issue_number}: {str(e)}")
    
    print(f"Completed generating {total_issues} gallery HTML files in '{output_dir}' directory")

if __name__ == "__main__":
    # Configure the total number of issues
    TOTAL_ISSUES = 3
    
    # Generate all galleries
    generate_all_galleries(TOTAL_ISSUES)