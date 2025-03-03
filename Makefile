export VERSION := $(shell jq '.version' package.json)

build:
	docker compose build

up:
	VERSION="${jq '.version' package.json}" docker compose up serviz larcmacs

up-grsim:
	VERSION="${jq '.version' package.json}" docker compose up grsim

up-all:
	echo "VERSION=${VERSION}"
	docker compose up serviz larcmacs grsim

down:
	docker compose down
