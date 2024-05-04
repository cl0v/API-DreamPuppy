tag = 1.3.1

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

debug:
	docker build -t vianagallery/gallery-api:debug .

profile:
	docker build vianagallery/gallery-api:debug .
	docker buildx build --platform linux/amd64 --push -t vianagallery/gallery-api:profile .

stable:
	docker buildx build --platform linux/amd64 --push -t vianagallery/gallery-api:${tag} .
	docker buildx build --platform linux/amd64 --push -t vianagallery/gallery-api .

up:
	docker compose up -d --always-recreate-deps
down:
	docker compose down

# envon:
# 	source ../bin/activate

# envoff:
# 	deactivate

uvi: 
	uvicorn gallery_api_impl.main:app --reload --port=9900

rollout:
	kubectl rollout restart deployments/api -n backend