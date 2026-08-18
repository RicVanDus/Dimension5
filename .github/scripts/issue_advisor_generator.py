import os
import sys
import json
import urllib.request
import urllib.parse
from os.path import split
from typing import List, Dict, Optional, Any

import pydantic
from pydantic import BaseModel, Field

import spacy

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

    @property
    def category(self) -> str | None:
        category_names = [
            "Import",
            "Orders",
            "API",
            "Feed",
            "Quick fix",
            "first"
        ]
        for label in self.label_names:
            return next((item for item in category_names if item in label), None)
        return None


class SearchResult(BaseModel):
    total_count: int
    items: Optional[List[IssueData]] = []

# categories we want to search on
SEARCH_LABELS = ["first"]

# labels we want to include in the query
LABELS_TO_QUERY = {
    "Import": ["Tool", "Platform:"],
    "Orders": ["Tool"],
    "API": ["Tool"],
    "first": ["bug"]
}

# labels we don't want to show in the results view
LABELS_NOT_IN_VIEW = ["z_company", "Country:", "Waiting"]


class IssueAdvisor:
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


    def main(self):
        self.get_event_data()
        comment_text = self.generate_search_result(
            current_issue= self.get_current_issue_data()
        )

        # if there's a comment generated, write output to GITHUB_OUTPUT environment
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output and comment_text:
            with open(github_output, 'w') as f_comment:
                f_comment.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")


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


    def generate_search_result(self, current_issue: IssueData) -> str:
        """
        We make 2 different search results: broad search & company related issues (TODO).
        Both are filtering on the Tool Section label and the company on its company_id label.

        This generates Github comment content with the search results presented in tables.

        If there are no search results (empty string returns) the action won't post the comment.
        """
        comment = ""

        if not current_issue.category in SEARCH_LABELS:
            return comment

        search_result, search_url = self._make_search_query(current_issue)

        # filter out this issue
        filtered_items = [
            item for item in search_result.items
            if item.number != self.issue_number
        ]

        list1 = [1, 2, 3, 4]
        list2 = [4, 5, 6, 7]

        has_common_value = any(item in set(list2) for item in list1)

        print(has_common_value)  # True

        if filtered_items:
            comment = "### Possible related issues: \n "

            for issue in filtered_items:
                new_link = issue.html_url.replace("/github", "/www.github")
                is_open = issue.state == "open"
                status_icon = "◯" if is_open else "●"

                comment += f"| {status_icon} | [{issue.title}]({new_link}) | \n"
                comment += "| --- | :--- | \n"
                comment += f"| | {issue.updated_at.split("T")[0]} - "
                comment += " ".join(user.login for user in issue.assignees) + (
                    f" - {issue.comments} comments | \n"
                )
                if issue.labels:
                    comment += " | | "
                    for label in issue.labels:
                        if any(exc.lower() in label.name for exc in LABELS_NOT_IN_VIEW):
                            label_name = label.name.replace(" ", "_")
                            comment += (f"![{label.name}](https://img.shields.io/badge/"
                                        f"{label_name}-{label.color}?style=flat) ")
                    comment += "|"

                comment += "\n\n"

            result_amount = search_result.total_count - len(filtered_items)
            if result_amount > 0:
                comment += f"- **({result_amount}) more results:** {search_url}"
        else:
            comment = search_url

        return comment


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


    def _extract_keywords(self, title: str) -> set[str]:
        """
        split the title and filter on useful strings
        """
        nlp = spacy.load("en_core_web_sm")

        # split off the company name
        title_without_company = title.split(" - ")[1]

        doc = nlp(title_without_company)

        # Define POS tags that represent core domain concepts
        # NOUN = general objects/things
        # PROPN = proper nouns (e.g., framework names, services)
        _allowed_pos = {"NOUN", "PROPN"}

        return {
            word.text for word in doc
            if word.pos_ in _allowed_pos and not word.is_punct
        }


    def _make_search_query(
            self, current_issue: IssueData, company_related: bool = False
    ) -> tuple[SearchResult, str]:
        """
        extract the keywords from the title when doing a default
        """
        search_keywords = self._extract_keywords(current_issue.title)
        search_query = " ".join(search_keywords)
        search_labels = ""

        if labels_to_include := LABELS_TO_QUERY.get(current_issue.category):
            query_labels = [
                f'label:"{label}"'
                for label in current_issue.label_names
                if any(inc.lower() in label.lower() for inc in labels_to_include)
            ]
            search_labels = " ".join(query_labels)

        full_query = urllib.parse.quote(
            f"repo:{self.repo_owner}/{self.repo_name} is:issue {search_query} {search_labels}"
        )

        limit = 5
        limited_search_url = f"https://api.github.com/search/issues?q={full_query}&per_page={limit}"
        full_search_url = f"https://github.com/search?type=issues&q={full_query}"

        return self._make_request(limited_search_url, SearchResult), full_search_url




if __name__ == '__main__':
    issue_advisor = IssueAdvisor()
    issue_advisor.main()