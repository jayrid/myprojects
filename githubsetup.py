#!/usr/bin/env python3
import os
import subprocess

# Check if the SSH key file exists; if not, generate a new key pair
ssh_key_path = os.path.expanduser("~/.ssh/id_rsa_github")
if not os.path.isfile(ssh_key_path):
    subprocess.run(["ssh-keygen", "-f", ssh_key_path, "-q", "-N", ""])

# Set environment variables for GitHub username, email, and personal access token
username = "your_github_username"
email = "your_email@example.com"
token = "your_personal_access_token"

# Configure global Git settings
subprocess.run(["git", "config", "--global", "user.name", username])
subprocess.run(["git", "config", "--global", "user.email", email])

# Export the public key content
with open(f"{ssh_key_path}.pub", "r") as key_file:
    ssh_tmux_key = key_file.read()

# Create the "myprojects" directory
myprojects_dir = os.path.expanduser("~/myprojects")
os.makedirs(myprojects_dir, exist_ok=True)

# Navigate to the "myprojects" directory
os.chdir(myprojects_dir)

# Check if the directory is empty; if not, print a warning and exit
if os.listdir(myprojects_dir):
    print(f"Your {myprojects_dir} directory is not empty. Exiting.")
    exit()
else:
    print(f"{myprojects_dir} is empty. Excellent!")

# Use cURL to create a new GitHub repository named "myprojects"
subprocess.run(["curl", "-X", "POST", "-H", "Accept: application/vnd.github+json",
                "-H", f"Authorization: Bearer {token}",
                "https://api.github.com/user/repos",
                "-d", '{"name":"myprojects","description":"This is your first repo"}'])

# Add an SSH key to the GitHub repository for authentication
subprocess.run(["curl", "-X", "POST", "-H", "Accept: application/vnd.github+json",
                "-H", f"Authorization: Bearer {token}",
                f"https://api.github.com/repos/{username}/myprojects/keys",
                "-d", f'{{"title":"tmux_key","key":"{ssh_tmux_key}","read_only":false}}'])

# Clone the GitHub repository to the local "myprojects" directory using HTTPS
subprocess.run(["git", "clone", f"https://github.com/{username}/myprojects.git", "~/myprojects"])

# Create a file named $USERNAME.md in the "myprojects" directory
open(os.path.join(myprojects_dir, f"{username}.md"), 'w').close()

# Add entries to the .gitignore file
with open(os.path.join(myprojects_dir, ".gitignore"), 'w') as gitignore_file:
    gitignore_file.write("*.log\n*.key\nid_rsa*\n")

# Add, commit, and push the changes to the GitHub repository
os.chdir(myprojects_dir)
subprocess.run(["git", "add", "*"])
subprocess.run(["git", "commit", "-m", "Initial commit"])
subprocess.run(["git", "push", "origin", "HEAD"])

