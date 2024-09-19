#!/bin/bash

# Check for sudo/root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or use sudo."
    exit 1
fi

# Check if Python is installed
if ! [ -x "$(command -v python3)" ]; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if git is installed
if ! [ -x "$(command -v git)" ]; then
    echo "Git is not installed. Please install Git and try again."
    exit 1
fi

# Check if openai is installed
if ! [ -x "$(command -v openai)" ]; then
    echo "OpenAI CLI is not installed. Please install OpenAI CLI and try again."
    exit 1
fi

# Check if python-subprocess is installed
if ! [ -x "$(command -v python3 -m subprocess)" ]; then
    echo "Python subprocess module is not installed. Please install Python subprocess module and try again."
    exit 1
fi

# Make sure aic.py is executable
chmod +x aic.py

# Move the script to /usr/local/bin and rename it to 'aicommit'
cp aic.py /usr/local/bin/aicommit

# Ensure /usr/local/bin/aicommit is executable
chmod +x /usr/local/bin/aicommit

echo "Installation complete! You can now use 'aicommit' globally."