#!/bin/sh

# Check the installation path and permissions for Newman
if [ -d "/usr/local/lib/node_modules/newman" ]; then
    sudo rm -rf /usr/local/lib/node_modules/newman
fi

# Install Newman
npm update -g newman

# Check the installation path and permissions for Newman
if [ -d "/usr/local/lib/node_modules/newman" ]; then
    sudo rm -rf /usr/local/lib/node_modules/newman
fi

# Assuming nvm is installed, use it to install and use Node.js v16
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 16
nvm use 16





# Display Node.js version
echo "Using Node.js version: $(node -v)"
