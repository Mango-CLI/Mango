#!/bin/bash

# The installer for Mango

# Check for existing Mango installation
if command -v mango &> /dev/null || which mango &> /dev/null; then
    echo -e "\033[1;33mMango has already been installed!\e[0m"
    exit 1
fi
echo -e "\033[1;33mInstalling Mango...\e[0m"

# Identify where to put the mango executable
USER_HOME=$(eval echo ~"$SUDO_USER")
DefaultInstallPath="$USER_HOME/.local/bin"
read -p "Where do you want to install? (default: $DefaultInstallPath): " InstallPath
if [[ -z "$InstallPath" ]]; then
    InstallPath="$DefaultInstallPath"
else
    InstallPath=$(realpath "$InstallPath")
fi

if [[ -z "$InstallPath" ]]; then
    echo -e "\033[4;31mError: Invalid path\e[0m"
    echo -e "\033[1;33mInstallation aborted!\e[0m"
    exit 1
fi

# Validate path
if [[ ! -d "$InstallPath" ]]; then
    # echo -e "\033[4;31mError: The path '$InstallPath' does not exist!\e[0m"
    echo -e "\033[1;33mWarning: The path '$InstallPath' does not exist!\e[0m"
    read -p "Do you want to create it? (y/N): " CreatePath
    if [[ "$CreatePath" == "y" || "$CreatePath" == "Y" ]]; then
        mkdir -p "$InstallPath"
    else
        echo -e "\033[1;33mInstallation aborted!\e[0m"
        exit 1
    fi
fi

# Permission check
if [[ ! -w "$InstallPath" ]]; then
    echo -e "\033[4;31mError: No write permission for '$InstallPath'. Try running with sudo.\e[0m"
    exit 1
fi

# Check for PATH
if [[ ":$PATH:" != *":$(realpath "$InstallPath"):"* ]]; then
    echo -e "\033[1;33mGiven location not in system PATH!\e[0m"
    echo -e "\033[1;35mMake sure you append it later to use Mango\e[0m"
fi

# Copy the executable
cp -p "$(dirname "$(realpath "$0")")/src/mango" "$InstallPath/mango"
chmod +x "$InstallPath/mango"
echo -e "\033[0;32mMango has been installed to $InstallPath\e[0m"

if [[ ! -d "$USER_HOME/.mango" ]]; then
    # Copy the .mango folder to the home mango path
    cp -r "$(dirname "$(realpath "$0")")/.mango" "$USER_HOME"/.mango
    echo -e "\033[0;32mThe home mango has been set up in $USER_HOME/.mango\e[0m"
fi

echo -e "\033[1;4;33mInstallation complete! :)\e[0m"