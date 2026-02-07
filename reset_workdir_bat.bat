@echo off
SET WORKDIR=workdir

IF EXIST %WORKDIR% (
    echo Removing existing workdir...
    rmdir /s /q %WORKDIR%
)

mkdir %WORKDIR%
echo Workdir reset!
