@echo off
PUSHD ..

docker-compose up -d code --build
timeout 1
docker attach hw08-code-1

docker-compose down 

POPD