#!/bin/bash

sudo docker-compose kill utility
sudo docker rm --force utility
sudo docker rmi --force utility