from github import Github


class GithubCommentWriter:
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)

    def write_review_comments(self, pr_number: int, review_result: dict):
        pr = self.repo.get_pull(pr_number)

        summary = review_result.get("summary", "")
        issues = review_result.get("issues", [])

        body = f"## AI Code Review Summary\n\n{summary}\n\n"

        for issue in issues:
            body += (
                f"### [{issue['severity'].upper()}] {issue['title']}\n"
                f"- File: `{issue['file']}`\n"
                f"- Line: `{issue['line']}`\n"
                f"- Suggestion: {issue['suggestion']}\n\n"
            )

        pr.create_issue_comment(body)
