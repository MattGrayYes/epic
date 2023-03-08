#!/bin/bash

# Check version
if hostnamectl | grep -q "(buster)"; then
    echo Running on Buster... yes
else
    echo "This script is made for Debian Buster, please do the install manually." 
    echo "Or remove this check, I don't care."
    exit 1
fi

echo ""
echo "This script assumes bare Raspberry PI OS (Debian Buster)"
echo "It will do the following:"
echo "- Enable USB Shell (USB Serial Gadget)"
echo "- Enable HyperPixel 2.1"
echo "- Install the EPIC application (takes a while)"
echo "- Reboot"
echo ""
read -p "Do you want to continue? (y/n)" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Nn]$ ]]
then
    exit 0
fi

# Enable USB-Shell for recovery
# https://www.tal.org/tutorials/setup-raspberry-pi-headless-use-usb-serial-console
echo ""
echo "Enabling USB-Shell..."
echo 'dtoverlay=dwc2' | sudo tee -a /boot/config.txt
echo ' modules-load=dwc2,g_serial' | sudo tee -a /boot/cmdline.txt
sudo systemctl enable getty@ttyGS0.service

# Create code folder
cd /home/pi
mkdir code
cd code

# Install HyperPixel
# https://github.com/pimoroni/hyperpixel2r
echo ""
echo "Installing HyperPixel..."
cd /home/pi/code
git clone https://github.com/pimoroni/hyperpixel2r
cd hyperpixel2r
sudo ./install.sh

# Install EPIC
# https://github.com/Jeroen6/epic
echo ""
echo "Installing EPIC..."
cd /home/pi/code
git clone https://github.com/Jeroen6/epic.git
cd epic
chmod +x start-epic.sh
mkdir /home/pi/.config/autostart/
cp epic.desktop /home/pi/.config/autostart/
pip3 install -r requirements.txt

# Create desktop icons
cd /home//code/epic
cp start-epic.sh /home/pi/Desktop/
# Set icon positions
cd /home/pi/.config
mkdir pcmanfm
cd pcmanfm
mkdir LXDE-pi
echo -e "\n[start-epic.sh]\nx=160\ny=230\n" | tee -a /home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.conf
cd /home/pi

echo ""
echo "All finished, rebooting. Use install-comitup.sh to setup WiFi connection management"
sudo reboot