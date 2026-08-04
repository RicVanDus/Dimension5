import os
import sys
import json
import urllib.request
import urllib.parse
from os.path import split
from typing import List, Dict, Optional, Any

import pydantic
from pydantic import BaseModel, Field

# Dataclasses
class IssueUser(BaseModel):
    login: str
    id: int
    avatar_url: str


class IssueLabel(BaseModel):
    name: str
    color: str


class IssueData(BaseModel):
    number: int
    state: str
    body: str
    title: str
    labels: Optional[List[IssueLabel]] = []
    user: IssueUser
    comments: int
    html_url: str
    assignees: List[IssueUser] = []
    created_at: str
    updated_at: str

    @property
    def label_names(self) -> set[str]:
        return {label.name for label in self.labels}


class SearchResult(BaseModel):
    total_count: int
    items: Optional[List[IssueData]] = []


SEARCH_LABELS = [] #make a list of labels we want to filter on


class IssueAdvisor():
    """
    IssueAdvisor v1

    Generates search results on keywords from the issue title. Giving back links to possible related
    issues.
    """

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
        url = (f"https://api.github.com/repos/{self.repo_owner}/"
               f"{self.repo_name}/issues/{self.issue_number}")

        return self._make_request(url, IssueData)


    def generate_search_result(self, issue_data: IssueData) -> str:
        """
        We make 2 different search results: broad search & company related issues

        Both are filtering on the Tool Section label and the company on its company_id label

        We are showing a table of
        """
        comment = ""

        search_result, search_url = self._make_search_query(issue_data)

        # filter out this issue
        filtered_items = [
            item for item in search_result.items
            if item.number != self.issue_number
        ]

        if filtered_items:
            comment = "### Possible related issues: \n "

            for issue in filtered_items:
                new_link = issue.html_url.replace("/github", "/www.github")
                issue_icon = ":green_circle:" if issue.state == "open" else ":purple_circle:"

                comment += f"| {issue_icon} [{issue.title}]({new_link}) | \n"
                comment += "| :--- | \n"
                comment += f"| {issue.updated_at.split("T")[0]} - "
                comment += " ".join(user.login for user in issue.assignees) + " |"
                if issue.labels:
                    for label in issue.labels:
                        label_name = label.name.replace(" ", "_")
                        comment += (f"![{label.name}](https://img.shields.io/badge/"
                                    f"{label_name}-{label.color}?style=flat) ")
                    comment += "| \n"

            result_amount = search_result.total_count - len(filtered_items)
            if result_amount > 0:
                comment += f"- ({result_amount}) more results: {search_url}"

        return comment


    def _extract_keywords(self, title: str) -> set[str]:
        """
        split the title and filter on useful strings
        """
        search_words = title.split( " - ")[1] # remove company name

        return {
            word for word in search_words.split(" ")
            if len(word) >= 4 or word.isupper()
        }


    def _make_search_query(
            self, issue_data: IssueData, company_related: bool = False
    ) -> tuple[SearchResult, str]:
        """
        extract the keywords from the title when doing a default
        """
        search_keywords = self._extract_keywords(issue_data.title)

        search_query = " ".join(search_keywords)

        full_query = urllib.parse.quote(
            f"repo:{self.repo_owner}/{self.repo_name} is:issue {search_query}"
        )
        limit = 5
        full_search_url = f"https://api.github.com/search/issues?q={full_query}"
        limited_search_url = full_search_url + f"&per_page={limit}"

        return self._make_request(limited_search_url, SearchResult), full_search_url


    def main(self):
        self.get_event_data()
        comment_text = self.generate_search_result(
            issue_data= self.get_current_issue_data()
        )

        # if there's a comment generated, write output to GITHUB_OUTPUT environment
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output and comment_text:
            with open(github_output, 'w') as f_comment:
                # We use multiline formatting in case your python string contains newlines
                f_comment.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")


if __name__ == '__main__':
    issue_advisor = IssueAdvisor()
    issue_advisor.main()