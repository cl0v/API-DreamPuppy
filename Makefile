tag = alp-0.0.5

build:
	docker build -t vianagallery/gallery-api:${tag} .
push:
	docker push vianagallery/gallery-api:${tag}
inspect:
	docker image inspect vianagallery/gallery-api:${tag}
run:
	docker container run vianagallery/gallery-api:${tag}
compose:
	docker compose up