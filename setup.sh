#!/bin/sh

# Install Python dependencies
pip3 install Flask pytest

# Check if NVM_DIR is defined
if [ -z "$NVM_DIR" ]; then
    export NVM_DIR="$HOME/.nvm"
fi

# Check if nvm.sh exists
if [ -s "$NVM_DIR/nvm.sh" ]; then
    # Source nvm in current shell
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    # Install the latest version of Node.js
    nvm install --lts

    # Use the latest LTS version
    nvm use --lts
else
    echo "NVM is not installed. Please install NVM to manage Node.js versions."
fi

# Install Newman globally
npm install -g newman

# Check Newman version
newman --version

# Additional setup steps as needed

