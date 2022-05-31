#!/bin/bash
#
# HASviolet_websox.sh
#
#   REVISION: 20210312-1400
#
# DESCRIPTION
#
#     This is a shell script that runs HASviolet_websox.py on startup.
#
#
# INSTALL THE SERVICE
#
#     ./HASviolet_websox.sh install
#
# STOP THE SERVICE
#
#     ./HASviolet_websox.sh stop
#
# START THE SERVICE
#
#     ./HASviolet_websox.sh start
#
# STATUS OF SERVICE
#
#     ./HASviolet_websox.sh status
#
# REMOVE THE SERVICE
#
#     ./HASviolet_websox.sh remove
#


# HASviolet Directory tree
HASVIOLET_REPO="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"
HASVIOLET_HOME=$HOME/HASviolet
HASVIOLET_ETC=$HOME/.config/HASviolet
HASVIOLET_CONFIG=$HASVIOLET_ETC/HASviolet.json
HASVIOLET_SSL_KEY=$HASVIOLET_ETC/HASviolet.key
HASVIOLET_SSL_crt=$HASVIOLET_ETC/HASviolet.crt
HASVIOLET_BANNER_COLOR="\e[0;104m\e[K"   # blue
HASVIOLET_BANNER_RESET="\e[0m"


case $1 in
    status)
        sudo systemctl status HASviolet_websox.service
        ;;
    start)
        sudo systemctl start HASviolet_websox.service
        ;;
    stop)
        sudo systemctl stop HASviolet_websox.service
        ;;
    remove)
        sudo systemctl stop HASviolet_websox.service
        sudo systemctl disable HASviolet_websox.service
        sudo rm -rf /lib/systemd/system/HASviolet_websox.service
        ;;
    install)
        sudo cp $HASVIOLET_HOME/HASviolet_websox.service /lib/systemd/system/HASviolet_websox.service
        sudo chown root:root /lib/systemd/system/HASviolet_websox.service
        sudo chmod 644 /lib/systemd/system/HASviolet_websox.service
        sudo systemctl daemon-reload
        sudo systemctl enable HASviolet_websox.service
        sudo systemctl start HASviolet_websox.service
        ;;
    *)
        echo "Usage: $0 {start | stop | kill}"
        echo "   start    : Start service"
        echo "   stop     : Stop Service"
        echo "   status   : Service Status"
        echo "   remove   : Nuke Service"
        ;;
esac