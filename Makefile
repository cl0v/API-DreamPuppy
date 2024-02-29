tag = 0.0.7

build:
	docker build --platform linux/arm64 -t vianagallery/gallery-api:develop .
bash:
	docker run --entrypoint "/bin/sh" -it gallery
push:
	docker build  --platform linux/amd64  -t vianagallery/gallery-api:a.${tag} .
	docker push vianagallery/gallery-api:a.${tag}
inspect:
	docker image inspect vianagallery/gallery-api:${tag}
run:
	docker container run vianagallery/gallery-api:develop
compose:
	docker compose up

backup:
	docker build --platform=linux/arm64 -t vianagallery/gallery-api:b.${tag} .
	docker push vianagallery/gallery-api:b.${tag}

profile:
	docker build --platform=linux/arm64 -t vianagallery/gallery-api:profile .
	docker push vianagallery/gallery-api:profile

stable: backup
	docker build --platform=linux/arm64 -t vianagallery/gallery-api:stable .
	docker push vianagallery/gallery-api:stable
