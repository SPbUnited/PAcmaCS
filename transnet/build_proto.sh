#!/bin/env bash

TARGETS="common erforce grsim"

for target in $TARGETS; do
    echo "Building $target"
    pushd proto/$target
    protoc --python_out=../../$target/pb *.proto
    popd
    FILES=$(find proto/$target -name "*.proto")
    echo $FILES
    protol \
        --create-package \
        --in-place \
        --python-out $target/pb \
        protoc --proto-path=proto/$target $FILES
done
