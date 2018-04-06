#!/bin/bash

docker stop onecut-docker
docker rm onecut-docker
docker build -t onecut:latest .
