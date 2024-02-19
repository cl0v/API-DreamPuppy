build:
	docker build --platform linux/amd64 -t vianagallery/gallery-api:alp-0.0.4 .
push:
	docker push vianagallery/gallery-api:alp-0.0.4
