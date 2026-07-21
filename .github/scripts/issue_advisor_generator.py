import os
import sys
import json

def main():

    # read contents of the issue
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not event_path:
        print("Error: No 'GITHUB_EVENT_PATH' set.")
        sys.exit(1)

    with open(event_path, 'r', encoding='utf-8') as f_issue:
        event_data = json.load(f_issue)

    # Access issue contents
    issue = event_data.get('issue', {})
    issue_title = issue.get('title', '')
    issue_body = issue.get('body', '')
    issue_author = issue.get('user', {}).get('login', '')

    # Example logic: Generate text based on conditions, API calls, etc.
    # Replace this with your actual logic
    comment_text = json.dumps(issue, indent=4)

    # If you decide NOT to send a reply, set comment_text to empty string ""
    # comment_text = ""

    # Write output to GITHUB_OUTPUT environment file so GitHub Actions can read it
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output and comment_text:
        with open(github_output, 'w') as f_comment:
            # We use multiline formatting in case your python string contains newlines
            f_comment.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")

if __name__ == '__main__':
    main()