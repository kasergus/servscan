#!/bin/bash

sudo docker build -t utility .
sudo docker-compose up -d

sudo docker exec utility pip install -r /utility/requirements.txt
echo "Do you want to run the server? [y/n]"
read answer
if [[ $answer == y ]]
then
	./run_server.sh
fi