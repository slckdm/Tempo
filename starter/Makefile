ROOT_DIRECTORY := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

COMPOSE_FILES := \
	$(ROOT_DIRECTORY)/starter/docker-compose.yaml \
	$(ROOT_DIRECTORY)/management/docker-compose.yaml \
	$(ROOT_DIRECTORY)/metadata/docker-compose.yaml \
	$(ROOT_DIRECTORY)/streaming/docker-compose.yaml \
	$(ROOT_DIRECTORY)/library/docker-compose.yaml \
	$(ROOT_DIRECTORY)/frontend/docker-compose.yaml

DOWN_COMPOSE_FILES := \
	$(ROOT_DIRECTORY)/frontend/docker-compose.yaml \
	$(ROOT_DIRECTORY)/library/docker-compose.yaml \
	$(ROOT_DIRECTORY)/streaming/docker-compose.yaml \
	$(ROOT_DIRECTORY)/metadata/docker-compose.yaml \
	$(ROOT_DIRECTORY)/management/docker-compose.yaml \
	$(ROOT_DIRECTORY)/starter/docker-compose.yaml

.PHONY: up up-build down

define compose_up
	@set -e; \
	for compose_file in $(COMPOSE_FILES); do \
		docker compose -f "$$compose_file" up $(1) -d; \
	done
endef

up:
	$(call compose_up)

up-build:
	$(call compose_up,--build)

down:
	@exit_code=0; \
	for compose_file in $(DOWN_COMPOSE_FILES); do \
		docker compose -f "$$compose_file" down || exit_code=$$?; \
	done; \
	exit $$exit_code
