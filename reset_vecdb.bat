@echo off
SET VECSTORE=chroma_db

IF EXIST %VECSTORE% (
    echo Removing existing vector store...
    rmdir /s /q %VECSTORE%
)

mkdir %VECSTORE%
echo Vectore store has been reset!