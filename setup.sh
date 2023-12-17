#!/bin/sh

# Install Node.js 16.x using Node Version Manager (NVM)
# NVM allows you to manage multiple Node.js versions
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.nvm/nvm.sh  # Load NVM
nvm install 16       # Install Node.js 16.x
nvm use 16            # Use Node.js 16.x as the active version

# Install Newman globally using npm
npm install -g newman

# Install other npm packages if needed
# npm install package-name

# Print a message indicating that setup is complete
echo "Setup is complete."
