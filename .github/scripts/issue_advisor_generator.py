import os
import sys
import json
import urllib.request
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Dataclasses
class IssueUser(BaseModel):
    login: str

class IssueLabel(BaseModel):
    name: str
    color: str

class IssueData(BaseModel):
    body: str
    title: str
    labels: Optional[List[IssueLabel]] = []
    user: IssueUser

    @property
    def label_names(self) -> set[str]:
        return {label.name for label in self.labels}


def get_current_issue_data() -> IssueData:
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not event_path:
        print("Error: No 'GITHUB_EVENT_PATH' set.")
        sys.exit(1)

    github_token = os.getenv('GITHUB_TOKEN')

    # Get the repository info and issue number from the trigger event
    with open(event_path, 'r', encoding='utf-8') as f_event:
        event_data = json.load(f_event)

    repo_owner = event_data['repository']['owner']['login']
    repo_name = event_data['repository']['name']
    issue_number = event_data['issue']['number']

    """Fetch the current, up-to-date issue data from GitHub's REST API."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Actions-Script"
    }

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            print(f"Error: Can't fetch data for issue {issue_number}: status {response.status}")
            sys.exit(1)
        else:
            json_data = json.loads(response.read().decode('utf-8'))
            return IssueData.model_validate(json_data)


def extractKeywords():
    pass


def createBasicQuery():
    pass


def main():
    issue_data = get_current_issue_data()

    if "bug" in issue_data.label_names:
        comment_text = str(issue_data) + "\n ITS A BUG"
    else:
        comment_text = ""

    # if there's a comment generated, write output to GITHUB_OUTPUT environment file so GitHub Actions can read it
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output and comment_text:
        with open(github_output, 'w') as f_comment:
            # We use multiline formatting in case your python string contains newlines
            f_comment.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")

if __name__ == '__main__':
    main()