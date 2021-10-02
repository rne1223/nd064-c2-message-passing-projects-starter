#!/bin/bash
PROTO_FILE="locations.proto"
LDIR="$HOME/udaconnect/modules/location-service/app"
ADIR="$HOME/udaconnect/modules/api"
python3 -m grpc_tools.protoc -I "$LDIR" --python_out="$LDIR" --grpc_python_out="$LDIR" $PROTO_FILE
python3 -m grpc_tools.protoc -I "$LDIR" --python_out="$ADIR" --grpc_python_out="$ADIR" $PROTO_FILE 