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


##
## INIT VARIABLES 
##

hasviolet_install=$HOME/hasviolet


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
        sudo cp $hasviolet_install/HASviolet_websox.service /lib/systemd/system/HASviolet_websox.service
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