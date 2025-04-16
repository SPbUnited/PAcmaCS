export VERSION := $(shell jq '.version' package.json)
export DIV:= divB

# https://stackoverflow.com/a/78547267
export UID=$(shell id -u)
export GID=$(shell id -g)

# Colorful output
# https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux

# Black        0;30     Dark Gray     1;30
# Red          0;31     Light Red     1;31
# Green        0;32     Light Green   1;32
# Brown/Orange 0;33     Yellow        1;33
# Blue         0;34     Light Blue    1;34
# Purple       0;35     Light Purple  1;35
# Cyan         0;36     Light Cyan    1;36
# Light Gray   0;37     White         1;37

BLACK=\033[0;30m
RED=\033[0;31m
GREEN=\033[0;32m
ORANGE=\033[0;33m
BLUE=\033[0;34m
PURPLE=\033[0;35m
CYAN=\033[0;36m
LGRAY=\033[0;37m
DGRAY=\033[1;30m
LRED=\033[1;31m
LGREEN=\033[1;32m
YELLOW=\033[1;33m
LBLUE=\033[1;34m
LPURPLE=\033[1;35m
LCYAN=\033[1;36m
WHITE=\033[1;37m

# High Intensity
IBLACK=\033[0;90m
IRED=\033[0;91m
IGREEN=\033[0;92m
IYELLOW=\033[0;93m
IBLUE=\033[0;94m
IPURPLE=\033[0;95m
ICYAN=\033[0;96m
IWHITE=\033[0;97m

# Bold High Intensity
BIRED=\033[1;91m

NC=\033[0m # No Color

init: init_py init_npm
	@echo "\n${YELLOW}Don't forget to do ${WHITE}source venv/bin/activate${NC}"
	@echo "                   ~~~~~~~~~~~~~~~~~~~~~~~~"

init_py:
	@echo "${GREEN}============="
	@echo "| VENV INIT |"
	@echo "=============${NC}"
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

init_npm:
	@echo "${GREEN}============="
	@echo "| NPM  INIT |"
	@echo "=============${NC}"
	cd serviz/serviz_frontend && npm install

build:
	@echo "${BLUE}============="
	@echo "|   BUILD   |"
	@echo "=============${NC}"
	cd serviz/serviz_frontend && npm run build
	docker compose build

up: up-message
	docker compose up core

up-grsim: up-message
	docker compose up grsim

up-autoreferee: up-message
	docker compose up autoreferee

up-all: up-message
	# docker compose up serviz larcmacs grsim
	docker compose up core grsim autoreferee

up-message:
	@echo "${PURPLE}============="
	@echo "|    UP     |"
	@echo "=============${NC}"
	@echo "VERSION=${VERSION}"
	@echo "DIVISION=${DIV}"
	@echo "UID=${UID}"
	@echo "GID=${GID}"

npm-dev:
	@echo "${CYAN}============="
	@echo "|  NPM DEV  |"
	@echo "=============${NC}"
	cd serviz/serviz_frontend && npm run dev

down:
	@echo "${RED}============="
	@echo "|    DOWN   |"
	@echo "=============${NC}"
	docker compose down

purge:
	@echo "${BIRED}============="
	@echo "|   PURGE   |"
	@echo "=============${NC}"
	docker compose down -v
	docker compose rm -f
