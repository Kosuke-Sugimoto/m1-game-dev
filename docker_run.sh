#!/bin/bash

DOCKER_IMAGE_NAME=graffiti:v2
DOCKER_CONTAINER_NAME=graffiti_v2
CURRENT_WORKING_DIR=$(pwd)/
DATASET_DIR=/mnt/hdd1/Datasets/Raw/
CHECKPOINT_DIR=/mnt/hdd1/Checkpoints/

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
           --mount type=bind,src=$CHECKPOINT_DIR,dst=/work/checkpoint/ \
           $DOCKER_IMAGE_NAME
