#!/bin/sh

# Install Python dependencies
pip3 install Flask pytest

# Install nvm (Node Version Manager)
#curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

npm install -g newman

# Source nvm in current shell
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install the latest version of Node.js
nvm install node
nvm use node
