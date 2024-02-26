tag = stable

build:
	docker build --platform linux/arm64 -t vianagallery/gallery-api:develop .
push:
	docker build  --platform linux/amd64  -t vianagallery/gallery-api:alph-${tag} .
	docker push vianagallery/gallery-api:alph-${tag}
inspect:
	docker image inspect vianagallery/gallery-api:${tag}
run:
	docker container run vianagallery/gallery-api:${tag}
compose:
	docker compose up

backup:
	docker build --platform=linux/amd64 -t vianagallery/gallery-api:stable-${tag} .
	docker push vianagallery/gallery-api:stable-${tag}

profile:
	docker build --platform=linux/arm64 -t vianagallery/gallery-api:profile .
	docker push vianagallery/gallery-api:profile

stable: backup
	docker build --platform=linux/amd64 -t vianagallery/gallery-api:stable .
	docker push vianagallery/gallery-api:stable
