.DEFAULT_GOAL := all

IMAGE = imsdb
VOLUME = -v "$(PWD)/downloaded-scripts:/usr/src/app/downloaded-scripts"

build:
	docker build -t $(IMAGE) .

run:
	docker run -it --rm --name $(IMAGE) $(VOLUME) $(IMAGE)

all: clean build run

shell:
	docker run -it --rm --name $(IMAGE)-shell $(VOLUME) $(IMAGE) /bin/bash

clean:
	find downloaded-scripts -type f -delete
