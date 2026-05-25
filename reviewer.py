import json
from anthropic import Anthropic
from prompt import SYSTEM_PROMPT


class ClaudeReviewer:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def review_diff(self, diff_content: str):
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"请审查以下 Git Diff：\n\n{diff_content}"
                }
            ]
        )

        content = response.content[0].text

        try:
            return json.loads(content)
        except Exception:
            return {
                "summary": "解析失败",
                "raw": content
            }
