export VERSION := $(shell jq '.version' package.json)
export DIV:= divB

build:
	cd serviz/serviz_frontend && npm run build
	docker compose build

up:
	docker compose up serviz larcmacs

up-grsim:
	docker compose up grsim

up-all:
	echo "VERSION=${VERSION}"
	echo "DIVISION=${DIV}"
	docker compose up serviz larcmacs grsim

npm-dev:
	cd serviz/serviz_frontend && npm run dev

down:
	docker compose down
