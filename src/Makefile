tag = 1.1.4

build:
	docker build --platform linux/arm64 -t vianagallery/gallery-api:develop .
bash:
	docker run --entrypoint "/bin/sh" -it gallery
push:
	docker build  --platform linux/arm64  -t vianagallery/gallery-api:a.${tag} .
	docker push vianagallery/gallery-api:a.${tag}
inspect:
	docker image inspect vianagallery/gallery-api:${tag}
run:
	docker container run vianagallery/gallery-api:develop
compose:
	docker compose up

develop:
	docker build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:D${tag} .
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:develop .

profile:
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:p${tag} .
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:profile .

stable:
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:${tag} .
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/gallery-api:stable .

up:
	docker compose up -d --always-recreate-deps
down:
	docker compose down

# envon:
# 	source ../bin/activate

# envoff:
# 	deactivate

uvi: 
	../bin/uvicorn app.main:app --reload --port=9900
