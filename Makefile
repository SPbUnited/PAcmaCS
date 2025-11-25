export VERSION:=$(shell jq '.version' package.json)
export DIV:=divB# divC
export CTRL:=SIM# REAL

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

ARCH=$(shell dpkg --print-architecture)
# UBUNTU_CODENAME=$(shell . /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
UBUNTU_CODENAME=$(shell cat /etc/*release | grep --color=never -oP '(?<=DISTRIB_CODENAME=).*')
UNAME_S := $(shell uname -s)

guard_not_mac:
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		echo "${RED}This command does not support for MacOS${NC} (you can't run PAcmaCS in Docker)" 1>&2; \
		exit 1; \
	fi

install_docker: guard_not_mac no-sudo
	echo "${UBUNTU_CODENAME}"
	# Add Docker's official GPG key:
	sudo rm /etc/apt/sources.list.d/docker.list || true
	sudo apt update || true
	sudo apt install -y ca-certificates curl
	sudo install -m 0755 -d /etc/apt/keyrings
	sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
	sudo chmod a+r /etc/apt/keyrings/docker.asc

	# Add the repository to Apt sources:
	echo \
	"deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
	${UBUNTU_CODENAME} stable" | \
	sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update || true

	sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

post_install_docker: guard_not_mac no-sudo
	sudo groupadd docker || true
	sudo usermod -aG docker ${USER}
	@echo "newgrp docker"
	@echo "\n${YELLOW}Reboot your machine now${NC} (ignore if using WSL)"
	@newgrp docker

install_misc: guard_not_mac no-sudo
	sudo apt update || true
	sudo apt install -y python3-venv npm jq vite

install: guard_not_mac install_misc install_docker post_install_docker

install_wsl: install_misc
	@echo "\n${YELLOW}Now please install Docker Desktop from ${WHITE}https://www.docker.com/products/docker-desktop/${NC}\n"

init: init_py init_npm
    mkdir -p logs

init_py: no-sudo
	@echo "${GREEN}============="
	@echo "| VENV INIT |"
	@echo "=============${NC}"
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

init_npm: no-sudo
	@echo "${GREEN}============="
	@echo "| NPM  INIT |"
	@echo "=============${NC}"
	cd serviz/frontend && npm install

build_docker: guard_not_mac no-sudo
	@echo "${BLUE}============="
	@echo "|   BUILD DOCKER   |"
	@echo "=============${NC}"
	docker compose build

build: guard_not_mac build_docker

up: up-message no-sudo
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		echo "Run for MacOS"; \
		source venv/bin/activate; \
		honcho start; \
	else \
		echo "Run for Debian system"; \
		docker compose up pacmacs serviz_frontend; \
	fi

up-grsim: guard_not_mac up-message no-sudo
	docker compose up grsim

up-autoreferee: guard_not_mac up-message no-sudo
	docker compose up autoreferee

up-all: guard_not_mac up-message no-sudo
	docker compose up pacmacs serviz_frontend grsim autoreferee

up-message:
	@echo "${PURPLE}============="
	@echo "|    UP     |"
	@echo "=============${NC}"
	@echo "VERSION=${VERSION}"
	@echo "DIVISION='${DIV}'"
	@echo "CONTROL=${CTRL}"
	@echo "UID=${UID}"
	@echo "GID=${GID}"

down: guard_not_mac
	@echo "${RED}============="
	@echo "|    DOWN   |"
	@echo "=============${NC}"
	docker compose down

purge: guard_not_mac
	@echo "${BIRED}============="
	@echo "|   PURGE   |"
	@echo "=============${NC}"
	docker compose down -v --remove-orphans
	docker compose rm -f

no-sudo:
	@{ \
	if [ "${UID}" -eq 0 ]; \
	then echo "${BIRED}Please run without SUDO${NC}"; \
	exit 1; \
	fi \
	}

