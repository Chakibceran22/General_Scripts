#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Updating Discord...${NC}"

# Check how Discord is installed
if snap list 2>/dev/null | grep -q discord; then
    echo "Discord installed via Snap"
    sudo snap refresh discord
elif flatpak list 2>/dev/null | grep -q discord; then
    echo "Discord installed via Flatpak"
    flatpak update -y com.discordapp.Discord
else
    echo "Downloading latest Discord .deb package..."
    # Use Downloads folder
    DOWNLOAD_DIR="$HOME/Downloads"
    cd "$DOWNLOAD_DIR" || exit 1
    
    # Kill any running Discord instances first
    echo -e "${YELLOW}Stopping Discord if running...${NC}"
    pkill -9 discord 2>/dev/null
    sleep 1
    
    # Download new version
    wget -O discord.deb "https://discord.com/api/download?platform=linux&format=deb"
    
    if [ $? -eq 0 ]; then
        echo "Installing Discord..."
        # Use DEBIAN_FRONTEND to prevent interactive prompts
        sudo DEBIAN_FRONTEND=noninteractive dpkg -i discord.deb
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -f -y
        
        # Wait a moment for processes to finish
        sleep 2
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Discord updated successfully!${NC}"
            echo -e "${YELLOW}Cleaning up...${NC}"
            
            # Force remove even if file is in use
            rm -f discord.deb
            
            if [ ! -f discord.deb ]; then
                echo -e "${GREEN}Installation file removed.${NC}"
            else
                echo -e "${YELLOW}Warning: Could not remove discord.deb (file may be in use)${NC}"
            fi
        else
            echo -e "${RED}Installation failed. Keeping discord.deb for debugging.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Failed to download Discord${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Done!${NC}"
