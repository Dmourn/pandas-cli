
# If you use podman instead of docker, put the next block of comments in your path as `docker` 
# i.e. /usr/bin/local/docker. No idea who to attribute.

# #!/usr/bin/sh
# [ -e /etc/containers/nodocker ] || \
# echo "Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg." >&2
# exec /usr/bin/podman "$@"

CONT_CMD=docker

test-container:
	${CONT_CMD} build -t panda-test .

.PHONY: run
run:
	${CONT_CMD} run -it --rm panda-test:latest
clean:
	${CONT_CMD} system prune
