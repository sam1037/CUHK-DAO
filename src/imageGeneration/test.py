import json
from pathlib import Path

shareCodes = {
    "firstLLM": "",
    "1stEvalLLM": "",
    "2ndEvalLLM": "",
    "3rdEvalLLM": "",
}

# save the sharecode as json file

print(shareCodes)
issue_number = 5
shareCodesPath = Path(__file__).parent.parent.parent / "shareCodes" / str(issue_number)
shareCodesPath.mkdir(parents=True, exist_ok=True)
with open(shareCodesPath / f"{'another'}_{'modelHolder'}_{'imgModelHolder'}.json", 'w', encoding='utf-8') as f:
    json.dump(shareCodes, f, ensure_ascii=False, indent=4)