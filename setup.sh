#!/bin/sh

# Install nvm and load it
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install and use the latest Node.js version
nvm install node
nvm use node
nvm alias default node

# Ensure the PATH is correctly set for the new Node.js version
export PATH="$NVM_DIR/versions/node/$(node -v)/bin:$PATH"

# Install or upgrade Newman
npm install -g newman

# Display the Node.js version
echo "Using Node.js version: $(node -v)"
