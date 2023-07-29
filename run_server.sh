#!/bin/bash

sudo docker-compose up -d
sudo docker exec -d utility python3 /utility/utility_server.py

echo "Do you want to enter in the container? [y/n]"
read answer
if [[ $answer == y ]]
then
	sudo docker exec -ti utility /bin/bash
fi