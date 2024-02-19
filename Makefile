tag = 0.0.5

build:
	docker build -t vianagallery/gallery-api:${tag} .
	docker build -t vianagallery/gallery-api:develop .
push:
	docker build -t vianagallery/gallery-api:${tag} .
	docker push vianagallery/gallery-api:${tag}
inspect:
	docker image inspect vianagallery/gallery-api:${tag}
run:
	docker container run vianagallery/gallery-api:${tag}
compose:
	docker compose up
push-stable:
	docker build -t vianagallery/gallery-api:alph-${tag} .
	docker push vianagallery/gallery-api:alph-${tag}
	docker build -t vianagallery/gallery-api:stable .
	docker push vianagallery/gallery-api:stable
