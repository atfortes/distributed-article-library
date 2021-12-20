#!/bin/bash

# create docker network hadoop
sudo docker network create --driver=bridge hadoop

# the default node number is 3
N=${1:-3}

# start hadoop master container
sudo docker rm -f hadoop-master > /dev/null
echo "start hadoop-master container..."
sudo docker run -itd \
           --net=hadoop \
           -p 9870:9870 \
           -p 8088:8088 \
           --name hadoop-master \
           --hostname hadoop-master \
           hadoop:3.2.1 > /dev/null

# start hadoop slave containers
i=1
while [ $i -lt $N ]
do
    sudo docker rm -f hadoop-slave$i > /dev/null
    echo "start hadoop-slave$i container..."
    sudo docker run -itd \
               --net=hadoop \
               --name hadoop-slave$i \
               --hostname hadoop-slave$i \
               hadoop:3.2.1 > /dev/null
    i=$(( $i + 1 ))
done 

# get into hadoop master container
sudo docker exec -it hadoop-master bash
