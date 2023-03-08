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
echo "- Install comitup WiFi-manager (takes a while)"
echo "- Reboot"
echo "You will lose SSH connection, it will reboot automatically"
echo "and come up in AP mode EPIC-nnn for you to connect to and setup wifi."
echo ""
read -p "Do you want to continue? (y/n)" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Nn]$ ]]
then
    exit 0
fi

# Install Comitup
# https://github.com/davesteele/comitup
    #1: Install the comitup package. It is included in Stretch and newer.
mkdir -pv /home/pi/comitup
pushd /home/pi/comitup
wget https://davesteele.github.io/comitup/latest/davesteele-comitup-apt-source_latest.deb
sudo dpkg -i --force-all davesteele-comitup-apt-source_latest.deb
rm davesteele-comitup-apt-source_latest.deb
sudo apt-get update
sudo apt-get install comitup comitup-watch -y
popd

    #2: Allow NetworkManager to manage the wifi interfaces by removing references to them from /etc/network/interfaces.
mkdir -pv /home/pi/.ciusafe/etc/network/interfaces
sudo cp -rv /etc/network/interfaces /home/pi/.ciusafe/etc/network/interfaces
sudo rm /etc/network/interfaces

    #3: Rename or delete /etc/wpa_supplicant/wpa_supplicant.conf.
mkdir -pv /home/pi/.ciusafe/etc/wpa_supplicant
mv -v  /etc/wpa_supplicant/wpa_supplicant.conf /home/pi/.ciusafe/etc/wpa_supplicant/wpa_supplicant.conf

# Change ap-name
echo 'ap_name=EPIC-<nnn>' | sudo tee -a /etc/comitup.conf

# Create desktop icon
cd /home/pi/Desktop
echo "comitup-cli d" >> forget-wifi.sh
chmod +x forget-wifi.sh
# Set icon positions
cd /home/pi/.config
mkdir pcmanfm
cd pcmanfm
mkdir LXDE-pi
echo -e "\n[forget-wifi.sh]\nx=320\ny=230\n" | tee -a /home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.conf

    #4: The systemd.resolved service should be disabled and masked to avoid contention for providing DNS service.
sudo systemctl mask dnsmasq.service
sudo systemctl mask systemd-resolved.service
sudo systemctl mask dhcpd.service
sudo systemctl mask dhcpcd.service
sudo systemctl mask wpa-supplicant.service

    #5: The line dns=dnsmasq should not be in /etc/NetworkManager/NetworkManager.conf.
#above

    #6: Comitup uses a local configuration of the DHCP setup utility dnsmasq to handle the network configuration of devices connecting to the Comitup hotspot. If another service is camped on the DHCP port (67) for the hotspot wifi interface, Comitup's dnsmasq will not be able to start, and connected devices may not be able to negotiate a useful IP address (this contention can also happen on the DNS port, 53). If this happens, the host port needs to be freed up. This may be fixed by masking the global dnsmasq.service ("systemctl mask dnsmasq.service"), or by disabling DHCP/DNS service on the HOTSPOT interface.
#grep this:

#7: Reboot.
echo "All done, rebooting"
sudo reboot