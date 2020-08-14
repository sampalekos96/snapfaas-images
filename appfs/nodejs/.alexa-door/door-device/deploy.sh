#!/bin/bash

SRC_DIR=$PWD
echo $SRC_DIR
ALEXA_SMARTHOME_PORT_DOOR=3456

echo "1. building smarthome device images"
if [[ ! $(docker images | grep smartdevice) ]]; then
    docker build -t smartdevice $SRC_DIR
fi

echo "2. running smarthome device containers"
if [[ ! $(docker ps | grep smartdevice) ]]; then
    docker run -p $ALEXA_SMARTHOME_PORT_DOOR:8080 -e DEVICE_NAME=door -d --rm --name door smartdevice
fi

#echo "3. creating reminder database..."
#couchdb_url=http://$COUCHDB_USERNAME:$COUCHDB_PASSWORD@$COUCHDB_IP:$COUCHDB_PORT
#curl -X PUT $couchdb_url/$ALEXA_REMINDER_COUCHDB_DATABASE
