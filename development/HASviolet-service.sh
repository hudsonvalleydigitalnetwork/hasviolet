#!/bin/bash
#
# HASviolet-service.sh
#
#


case $1 in
    start)
        sudo systemctl daemon-reload
        sudo systemctl enable HASviolet.service
        ;;
    stop)
        sudo systemctl stop HASviolet.service
        ;;
    remove)
        sudo systemctl stop HASviolet.service
        sudo systemctl disable HASviolet.service
        sudo rm -rf /lib/systemd/system/HASviolet.service
        ;;
    *)
        echo "Usage: $0 {start | stop | kill}"
        echo "   start    : Start service"
        echo "   stop     : Stop Service"
        echo "   remove     : Nuke Service"
        ;;
esac