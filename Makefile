build:
	docker compose build

up:
	docker compose up serviz larcmacs

up-grsim:
	docker compose up grsim

up-all:
	docker compose up serviz larcmacs grsim

down:
	docker compose down
