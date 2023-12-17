#!/bin/sh

# Create a virtual environment for Python
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
pip install Flask pytest

# Install Newman globally
npm install -g newman

# Check Newman version
newman --version
