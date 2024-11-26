#!/bin/sh
REPOSITORY_NAME=tyronextian/
IMAGE_NAME=apisix
TAG=3.10.0-debian

docker build -t ${IMAGE_NAME}:${TAG} -f Dockerfile .
docker tag ${IMAGE_NAME}:${TAG} ${REPOSITORY_NAME}${IMAGE_NAME}:${TAG}
docker push ${IMAGE_NAME}:${TAG}

echo "docker pull ${REPOSITORY_NAME}${IMAGE_NAME}:${TAG}"