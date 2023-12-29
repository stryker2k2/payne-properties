#!/bin/bash

# - Ensure that `install_requirements.sh` is executable (via `chmod +x`)
# - Install using Python Virtual Environment (`source venv/bin/activate`)

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

# Using 'install_requirements' Script to install Common Requirements
echo -e "${GREEN}\n[+] Installing Requirements${ENDCOLOR}"
sudo install_requirements.sh

# Installing APT Dependencies
echo -e "${GREEN}\n[+] Installing Server Specific Requirements${ENDCOLOR}"
sudo apt install apache2 -y
sudo apt install libapache2-mod-wsgi-py3 -y