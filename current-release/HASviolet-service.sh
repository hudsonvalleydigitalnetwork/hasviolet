#!/bin/bash
#
# HASviolet-service.sh
#
# 20200804-2134
#


case $1 in
    start)
        sudo systemctl start HASviolet.service
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