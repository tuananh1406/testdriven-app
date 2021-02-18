#!/bin/bash
export DOCKER_MACHINE_DEV_IP=$(docker-machine ip testdriven-dev)
export REACT_APP_USERS_SERVICE_URL=http://$DOCKER_MACHINE_DEV_IP
