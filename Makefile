# If you use podman instead of docker, put the next block of comments in your path as `docker` 
# i.e. /usr/bin/local/docker. No idea who to attribute.

# #!/usr/bin/sh
# [ -e /etc/containers/nodocker ] || \
# echo "Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg." >&2
# exec /usr/bin/podman "$@"


SOURCES=$(wildcard *.py) pandas_cli test
CONT_CMD=docker
CONT_NAME=panda-test

.PHONY: help
help:
	@printf "%-40s %s\n" "======" "==========="
	@printf "%-40s %s\n" "Target" "Description"
	@printf "%-40s %s\n" "======" "==========="
	@fgrep " ## " $(MAKEFILE_LIST) | fgrep -v grep  | awk -F ': .*## ' '{$$1 = sprintf("%-40s", $$1)} 1'

.env:
	@echo .env does not exist. Creating...
	python3 -m venv .env 

.PHONY: dev-env
dev-env: .env
	source .env/bin/activate && \
		pip install -U --no-cache pip && pip install -r dev-requirements.txt

container: ## Build in a container
	${CONT_CMD} build -t ${CONT_NAME} .

.PHONY: run-container
run-container: ## Run the container from test-container
	${CONT_CMD} run -it --rm ${CONT_NAME}:latest

clean-container: ## Docker system prune and remove the test container
	${CONT_CMD} system prune
	${CONT_CMD} rmi ${CONT_NAME}

.PHONY: clean
clean: ## Clean the things
	rm -rfv ./.nox
	rm -rfv ./build
	rm -r pandas_cli.egg-info

.PHONY: test-black
test-black: ## Check the diff for black
	black --color --check --diff $(SOURCES)

.PHONY: black
black: ## Run black
	black $(SOURCES)
