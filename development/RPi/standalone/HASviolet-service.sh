#!/bin/bash
#
# HASviolet-service.sh
#
#
doit=$1
case doit in
    start)
        sudo systemctl daemon-reload
        sudo systemctl enable HASviolet.service
        ;;
    stop)
        sudo systemctl stop HASviolet.service
        ;;
    *)
        echo "Usage: $0 {start | stop}"
        echo "   start    : Start service"
        echo "   stop     : Stop Service"
        ;;
esac