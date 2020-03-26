#!/bin/bash

###
### HASviolet-update.py
###

##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/HVDN-repo

# HASviolet LocalRepo (GitHub clone)
hasviolet_localrepo=$HOME/HVDN-repo/hasviolet

# HASviolet Working directory
hasviolet_install=$HOME/HASviolet

# HASviolet Dev Directoy
hasviolet_dev=$HOME/DEVviolet

# HASviolet INI file
hasviolet_ini=$hasviolet_install/HASviolet.ini

# HASviolet GitHub Repo
hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"


##
##  START 
##

echo " "
echo "HASviolet-update"
echo " "

echo " "
echo "- Backing up your ini file"
echo " "

cp /home/pi/HASviolet/HASviolet.ini /home/pi/HASviolet.ini.bk1

echo " "
echo "- Nuking HASviolet directories and local HVDN repo"
echo " "

sudo rm -rf /home/pi/HVDN-repo
sudo rm -rf /home/pi/HASviolet

if [ "$1" == "dev" ]; then
  sudo rm -rf /home/pi/DEVviolet
fi

echo " "
echo "- Clone HASviolet Repository"
echo " "

mkdir $hvdn_localrepo
cd $hvdn_localrepo
git clone $hasviolet_github_repo

echo " "
echo "- Create HASviolet working directory"
echo " "

mkdir $hasviolet_install
cp -R $hasviolet_localrepo/stable/* $hasviolet_install

echo " "
echo " Restore your ini file"
echo " "

rm $hasviolet_install/HASviolet.ini
cp /home/pi/HASviolet.ini.bk1 $hasviolet_install/HASviolet.ini

if [ "$1" == "dev" ]; then
  echo " "
  echo "- Create HASviolet DEV working directory"
  echo " "
  
  mkdir $hasviolet_dev
  cp -R $hasviolet_localrepo/development/RPi/* $hasviolet_dev
  
  echo " "
  echo " Copy your ini file into DEV working directory"
  echo " "
  
  rm $hasviolet_dev/HASviolet.ini
  cp /home/pi/HASviolet.ini.bk1 $hasviolet_dev/HASviolet.ini
fi

rm /home/pi/HASviolet.ini.bk1

echo " "
echo "HASviolet installation complete."
echo " "
echo "- The HASviolet repo has been cloned to $hasviolet_localrepo"
echo "- A working directory with all apps is installed in $hasviolet_install"
echo "- Check your HASviolet.ini it should have been restored"
echo " "
echo "To run the apps, you must be in the $hasviolet_install directory and"
echo "prefix the app name with ./<app-name>"
echo " "
echo "for example:       ./HASviolet-rx.py"
echo " "

echo " "
echo "Enjoy! -- The HASviolet Team at HVDN "
echo " "
echo " "

sleep 3
exit 0