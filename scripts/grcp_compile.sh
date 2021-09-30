#!/bin/bash
DIR='./modules/location-service/app'
python3 -m grpc_tools.protoc -I "$DIR" --python_out="$DIR" --grpc_python_out="$DIR" locations.proto