import json
import re


def parse_tool_call(response: str):
    """Extract a tool-call JSON object from the LLM's raw text response.

    Handles the ideal case (response is pure JSON) as well as common
    LLM quirks: JSON wrapped in ```json ... ``` code fences, or JSON
    preceded/followed by extra explanatory text.
    """

    if not response:
        return None

    text = response.strip()

    # Strip markdown code fences like ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # Build a list of candidate strings to try parsing as JSON:
    # 1) the cleaned text as-is
    # 2) the first {...} block found anywhere in the text
    candidates = [text]

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidates.append(match.group(0))

    for candidate in candidates:
        try:
            tool_request = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        except Exception:
            continue

        if not isinstance(tool_request, dict):
            continue
        if "tool" not in tool_request:
            continue
        if not isinstance(tool_request["tool"], str):
            continue

        return tool_request

    return None


if __name__ == "__main__":
    tests = [
        '{ "tool" : "calculator", "expression" : "25**2" }',
        '```json\n{ "tool":"weather", "city":"New Delhi" }\n```',
        'Sure, here is the tool call:\n{ "tool":"weather", "city":"New Delhi" }',
        'hello how are you',
    ]

    for t in tests:
        print(repr(t[:50]), "->", parse_tool_call(t))
