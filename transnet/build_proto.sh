#!/bin/env bash

# print commands
set -x
# exit on error
set -e

PROTO_PATH=../ssl_packet_package/proto/ssl
PYOUT_PATH=./protopy
FILES=$(find ../ssl_packet_package/proto/ssl -name '*.proto')

mkdir -p $PYOUT_PATH

python3 -m grpc_tools.protoc -I$PROTO_PATH --pyi_out=$PYOUT_PATH $FILES
python3 -m grpc_tools.protoc -I$PROTO_PATH --python_out=$PYOUT_PATH $FILES

# Generate FileDescriptorSet for protol import rewriting (no system protoc needed)
TMPFDS=$(mktemp)
python3 -m grpc_tools.protoc -I$PROTO_PATH --descriptor_set_out="$TMPFDS" --include_imports $FILES
protol \
    --create-package \
    --in-place \
    --python-out $PYOUT_PATH \
    raw "$TMPFDS"
rm -f "$TMPFDS"
