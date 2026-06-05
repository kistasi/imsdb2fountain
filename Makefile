IMAGE = imsdb
VOLUME = -v "$(PWD)/downloaded-scripts:/usr/src/app/downloaded-scripts"

build:
	docker build -t $(IMAGE) .

run:
	docker run -it --rm --name $(IMAGE) $(VOLUME) $(IMAGE)

all: build run

shell:
	docker run -it --rm --name $(IMAGE)-shell $(VOLUME) $(IMAGE) /bin/bash
