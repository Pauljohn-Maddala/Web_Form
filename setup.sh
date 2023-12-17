#!/bin/sh

# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install the latest version of Node.js
nvm install node

# Use the installed Node.js version
nvm use node

# Update PATH to use the installed Node.js version
export PATH="$NVM_DIR/versions/node/$(node -v)/bin:$PATH"

# Display the Node.js version
echo "Using Node.js version: $(node -v)"

# Install Newman
npm install -g newman

# Install or upgrade Newman
npm install -g newman


echo "Using Node.js version: $(node -v)"
