#!/bin/bash

# Check for existing Mango installation
if ! command -v mango &> /dev/null && ! which mango &> /dev/null; then
    echo -e "\033[1;33mMango is not installed!\e[0m"
    exit 1
fi

echo -e "\033[1;33mUninstalling Mango...\e[0m"

# Ask for confirmation to remove the home mango folder
read -p "Do you want to remove the home mango folder? (y/N): " RemoveHomeMango
if [[ "$RemoveHomeMango" =~ ^[Yy]$ ]]; then
    USER_HOME=$(eval echo ~"$SUDO_USER")
    if [[ ! -d "$USER_HOME/.mango" ]]; then
        echo -e "\033[1;33mThe home mango folder does not exist\e[0m"
    fi
    rm -rf "$USER_HOME/.mango"
    echo -e "\033[1;32mThe home mango has been removed\e[0m"
else
    echo -e "\033[0;33mThe home mango is kept\e[0m"
fi

# Remove the executable
rm -f "$(which mango)"
echo -e "\033[1;4;33mMango has been uninstalled :)\e[0m"