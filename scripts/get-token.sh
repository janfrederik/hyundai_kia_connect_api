#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver

# Setup and run
source .venv/bin/activate
uv add --no-install-project selenium requests webdriver-manager

# Download and run script
wget -O scripts/HyundaiFetchApiTokensSelenium.py https://gist.githubusercontent.com/chrisf4lc0n/d5506bd69e0d07b53574442c972090fe/raw/
uv run python scripts/HyundaiFetchApiTokensSelenium.py
