#!/usr/bin/env python3
import openai
import subprocess

# Read OpenAI API key from /etc/openai.key
def read_api_key():
    try:
        with open('/etc/openai.key', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API key file not found. Please ensure /etc/openai.key exists.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the API key: {str(e)}")
        exit(1)

# Set OpenAI API key
openai.api_key = read_api_key()

# Get the git diff
def get_git_diff():
    result = subprocess.run(['git', 'diff', '--staged'], stdout=subprocess.PIPE)
    diff = result.stdout.decode('utf-8')
    # Optionally truncate if too large
    max_length = 5000  # Adjust depending on token limits
    return diff[:max_length]

# Generate commit message using GPT-4 with the new OpenAI API
def generate_commit_message(diff):
    prompt = f"Generate a concise and descriptive git commit message based on the following diff:\n\n{diff}"
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that helps write git commit messages."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100
    )
    commit_message = response.choices[0].message.content;
    return commit_message.strip()

# Commit changes
def commit_changes(commit_message):
    subprocess.run(['git', 'commit', '-m', commit_message])

# Ask for user confirmation
def confirm_commit(commit_message):
    print(f"\nGenerated Commit Message:\n\n{commit_message}\n")
    confirm = input("Do you want to commit with this message? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        commit_changes(commit_message)
        print("Changes have been committed.")
    else:
        print("Commit aborted.")

if __name__ == "__main__":
    diff_content = get_git_diff()
    commit_message = generate_commit_message(diff_content)
    
    # Ask for confirmation and commit if the user agrees
    confirm_commit(commit_message)
