build:
# docker buildx build --platform linux/arm64,linux/amd64 --builder=container  -t vianagallery/migrations:latest .
	docker build --platform linux/arm64 -t vianagallery/migrations:develop .
	
push: build
	docker push vianagallery/migrations:develop

stable:
	docker buildx build --platform linux/arm64,linux/amd64 --builder=container --push -t vianagallery/migrations:latest .
