import os
import sys
import json
import urllib.request
import urllib.parse
from hmac import new
from typing import List, Dict, Optional, Any

import pydantic
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
    comments: int
    html_url: str

    @property
    def label_names(self) -> set[str]:
        return {label.name for label in self.labels}


class SearchResult(BaseModel):
    total_count: int
    items: Optional[List[IssueData]] = []


class IssueAdvisor():
    def __init__(self):
        self.event_path: str
        self.repo_owner: str
        self.repo_name: str
        self.issue_number: str
        self.github_token: str

    def get_event_data(self) -> None:
        event_path = os.getenv("GITHUB_EVENT_PATH")

        if not event_path:
            print("Error: No 'GITHUB_EVENT_PATH' set.")
            sys.exit(1)

        self.github_token = os.getenv('GITHUB_TOKEN')

        # Get the repository info and issue number from the trigger event
        with open(event_path, 'r', encoding='utf-8') as f_event:
            event_data = json.load(f_event)

        self.repo_owner = event_data['repository']['owner']['login']
        self.repo_name = event_data['repository']['name']
        self.issue_number = event_data['issue']['number']


    def _make_request(
            self, url: str,
            response_model: type[pydantic.BaseModel]
    ) -> Any:
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHub-Actions-Script"
        }

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"Wrong response from {url} - status {response.status}")
                sys.exit(1)
            else:
                json_data = json.loads(response.read().decode('utf-8'))
                return response_model.model_validate(json_data)


    def get_current_issue_data(self) -> IssueData:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues/{self.issue_number}"

        return self._make_request(url, IssueData)


    def extractKeywords(self):
        pass


    def generate_search_result(self, issue_data: IssueData) -> str:
        search_result = self._make_search_query(issue_data)
        comment = ""

        if search_result:
            comment = ("### Possible related issues: \n "
                       "--- \n")
            comment += "".join(f"- [{issue.title}]({issue.html_url})\n" for issue in search_result.items)

        return comment


    def _make_search_query(self, issue_data: IssueData) -> SearchResult:
        query = urllib.parse.quote(f"repo:{self.repo_owner}/{self.repo_name} is:issue test")
        limit = 5
        url = f"https://api.github.com/search/issues?q={query}&per_page={limit}"

        return self._make_request(url, SearchResult)


    def main(self):
        self.get_event_data()
        comment_text = self.generate_search_result(
            issue_data= self.get_current_issue_data()
        )

        # if there's a comment generated, write output to GITHUB_OUTPUT environment file so GitHub Actions can read it
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output and comment_text:
            with open(github_output, 'w') as f_comment:
                # We use multiline formatting in case your python string contains newlines
                f_comment.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")


if __name__ == '__main__':
    issue_advisor = IssueAdvisor()
    issue_advisor.main()