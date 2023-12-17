#!/bin/sh

# Install Python dependencies
pip3 install Flask pytest

# Check if nvm is installed, if not, install it
if ! command -v nvm &> /dev/null; then
    # Install nvm (Node Version Manager)
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    # Source nvm in current shell
    export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Check if nvm is sourced correctly
if [ -z "$NVM_DIR" ]; then
    echo "Error: nvm not sourced correctly"
    exit 1
fi

# Install the required Node.js version
nvm install 16

# Check if Node.js is installed successfully
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not installed correctly"
    exit 1
fi

# Use the installed Node.js version
nvm use 21

# Install Newman
npm install -g newman

# Check if Newman is installed successfully
if ! command -v newman &> /dev/null; then
    echo "Error: Newman not installed correctly"
    exit 1
fi

# Display the Node.js version being used
node -v

# Display the Newman version
newman -v

# Continue with the rest of your setup and tests
