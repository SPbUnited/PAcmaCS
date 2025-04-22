#!/bin/env bash

# print commands
set -x

PROTO_PATH=./proto
PYOUT_PATH=./protopy
FILES=$(find proto -name '*.proto')

echo $FILES

mkdir -p $PYOUT_PATH

protoc -I$PROTO_PATH --pyi_out=$PYOUT_PATH $FILES
protoc -I$PROTO_PATH --python_out=$PYOUT_PATH $FILES

protol \
    --create-package \
    --in-place \
    --python-out $PYOUT_PATH \
    protoc --proto-path=$PROTO_PATH $FILES


# TARGETS="api ci engine geom rcon state statemachine tracker vision"

# for target in $TARGETS; do
#     echo "Building $target"
#     pushd proto/$target
#     protoc --python_out=../../$target/pb *.proto
#     popd
#     FILES=$(find proto/$target -name "*.proto")
#     echo $FILES
#     protol \
#         --create-package \
#         --in-place \
#         --python-out $target/pb \
#         protoc --proto-path=proto/$target $FILES
# done
