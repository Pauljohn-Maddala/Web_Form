#!/bin/sh

# Install Python dependencies
pip3 install Flask pytest

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    # Install Node.js LTS version directly
    curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install Newman globally
npm install -g newman

# Check Newman version
newman --version
