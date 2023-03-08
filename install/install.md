# Installation
These two instllation scripts will help you install everything.

1. Create an image with the Raspberry Pi Imager and ensure the settings include provisioning for WiFi and SSH.
2. Boot the raspberry pi while attached to your PC with the OTG port.
2. Copy the install scripts to the boot folder.
3. Login over SSH 
4. Copy the scripts to the home directory
    - `cp /boot/install-* ./"
5. Run `./install-epic.sh`
6. Wait
7. Login over SSH or USB-Shell with putty.
8. Run ./install-comitup.sh` to install the tool to make changnig the wifi network possible.
    - This tool: https://github.com/davesteele/comitup
9. Wait for reboot.
10. Look for wifi `EPIC-###` on your phone and connect to it.
    - Captive portal should point you to you config page, otherwise http://10.41.0.1/ or the router IP comitup picks.
11. Enjoy!

Two scripts have been placed on the desktop to restart the epic application or forget the current wifi network.
When no network is found the unit will automatically go into AP mode for wifi configuration.
For recovery and other stuff the USB-Shell is enabled on then OTG port.