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
stable:
	docker build --platform=linux/amd64 -t vianagallery/gallery-api:${tag} .
	docker push vianagallery/gallery-api:${tag}
	docker build --platform=linux/amd64 -t vianagallery/gallery-api:stable .
	docker push vianagallery/gallery-api:stable
