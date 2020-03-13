#!/bin/bash
#
# HASviolet.service Install
#
#
# DESCRIPTION
#
#     This is a systemd service that runs HASviolet-duckhun.py on Pi startup.
#     Left button runs beacon, Middle button quits beacon
#     Right button is RX mode. Unfortunately only way to exit RX mode is to 
#     power off the Pi/
#
#
# INSTALLATION
#
#
echo " "
echo "HASviolet.service Install"
echo " "
echo "- Sudo privilege required"
echo " "

sudo cp /home/pi/hasviolet/HASviolet.service /lib/systemd/system/HASviolet.service
sudo chown root:root /lib/systemd/system/HASviolet.service
sudo chmode 644 /lib/systemd/system/HASviolet.service
sudo systemctl daemon-reload
sudo systemctl enable HASviolet.service
sudo sync

echo " "
echo "HASviolet.service installed"
echo " "
sleep 2
echo " **NOTE:** When logging in via shell you will need to stop the service to"
echo "           use HASviolet interactively during your session."
echo "           This can be done by executing the following:"
echo " "
echo "           ./HASviolet-service stop"
echo " "
echo "           When done with your session, you can either reboot the Pi or"
echo "            restart the service as follows:"
echo " "
echo "           ./HASviolet-service start"
echo " "
echo " "
echo " "
echo "System will reboot in fifteen seconds"
echo " "
sleep 15
sudo reboot
