import os
import subprocess
from dotenv import load_dotenv

from reviewer import ClaudeReviewer
from github_writer import GithubCommentWriter


load_dotenv()


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
PR_NUMBER = int(os.getenv("PR_NUMBER"))


# 获取 Git Diff
result = subprocess.run(
    ["git", "diff", "origin/main...HEAD"],
    capture_output=True,
    text=True
)


diff_content = result.stdout


if not diff_content.strip():
    print("No diff found")
    exit(0)


print("Reviewing diff...")

reviewer = ClaudeReviewer(ANTHROPIC_API_KEY)
review_result = reviewer.review_diff(diff_content)


print("Review Result:")
print(review_result)


writer = GithubCommentWriter(GITHUB_TOKEN, GITHUB_REPO)
writer.write_review_comments(PR_NUMBER, review_result)


print("PR comments published successfully")
