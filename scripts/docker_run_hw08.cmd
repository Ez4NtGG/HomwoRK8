@echo off
PUSHD ..\tests

docker run -it --rm  --name web_hw_08  --env-file ../.env lexxai/web_hw_08

rem docker volume ls
                    

POPD