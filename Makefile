export VERSION := $(shell jq '.version' package.json)
export DIV:= divB

build:
	docker compose build

up:
	docker compose up serviz larcmacs

up-grsim:
	docker compose up grsim

up-all:
	echo "VERSION=${VERSION}"
	echo "DIVISION=${DIV}"
	docker compose up serviz larcmacs grsim

down:
	docker compose down
