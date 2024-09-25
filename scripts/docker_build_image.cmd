@echo off
PUSHD ..

docker build . -t lexxai/web_hw_08
docker images

POPD