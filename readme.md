# Caltech Center for Time Domain Astronomy

## Deploy with Docker.
TODO: move to docker-compose.yml

### Create persistent volumes for db and media files (if it has not been created yet)
```bash
docker volume create cftda-db
docker volume create cftda-media
```

### build and start the container
```bash
docker build -t cftda-server -f Dockerfile  .
docker run -d -p 8005:8005 --restart always --name cftda-server -v cftda-db:/cftda-db -v cftda-media:/cftda-media -it cftda-server
# test-start:
docker run --rm -p 8005:8005 --name cftda-server -v cftda-db:/cftda-db -v cftda-media:/cftda-media -it cftda-server
```

You can attach (as root) to a running Docker container like this:
```bash
docker exec -u root -i -t cftda-server /bin/bash
```

If you have a (pre-)populated `sqlite3` db or want to reuse the one from this repo,
copy it over to the persistent volume:
```bash
cp db.sqlite3 /cftda-db
```

Analogously, do the same for the media files:
```bash
cp -r media/* /cftda-media
```
