#!/bin/bash

DOCKER_IMAGE_NAME=graffiti:v1
DOCKER_CONTAINER_NAME=graffiti
CURRENT_WORKING_DIR=$(pwd)/
DATASET_DIR=/mnt/hdd1/Datasets/Raw/

if [[ "$(docker images -q $DOCKER_IMAGE_NAME 2> /dev/null)" == ""  ]]
then
    docker build -t $DOCKER_IMAGE_NAME .
fi

docker run -it \
           --name $DOCKER_CONTAINER_NAME \
           --gpus all \
           --ulimit memlock=-1 \
           --ulimit stack=67108864 \
           --mount type=bind,src=$CURRENT_WORKING_DIR,dst=/work/ \
           --mount type=bind,src=$DATASET_DIR,dst=/work/dataset/ \
           $DOCKER_IMAGE_NAME
