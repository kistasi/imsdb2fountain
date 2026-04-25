docker build --no-cache -t imsdb .
docker run -it --rm --name imsdb -v "$(pwd)/downloaded-scripts:/usr/src/app/downloaded-scripts" imsdb
