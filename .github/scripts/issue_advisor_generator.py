import os
import sys

def main():
    # Example logic: Generate text based on conditions, API calls, etc.
    # Replace this with your actual logic
    comment_text = "This comment comes from the python script."

    # If you decide NOT to send a reply, set comment_text to empty string ""
    # comment_text = ""

    # Write output to GITHUB_OUTPUT environment file so GitHub Actions can read it
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'w') as f:
            # We use multiline formatting in case your python string contains newlines
            f.write(f"comment_body<<EOF\n{comment_text}\nEOF\n")

if __name__ == '__main__':
    main()