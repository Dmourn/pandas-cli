
test-container:
	podman build -t panda-test .

.PHONY: run
run:
	podman run -it --rm panda-test:latest
clean:
	podman system prune
