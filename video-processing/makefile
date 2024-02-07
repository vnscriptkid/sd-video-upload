build:
	docker build --platform linux/amd64 -f Dockerfile.local -t video-processing-service .

build_prod:
	docker build --platform linux/amd64 -t video-processing-service .

run:
	docker run -p 3000:3000 -d --name video-processing-service video-processing-service

rm:
	docker rm video-processing-service -f

rmi:
	docker rmi video-processing-service -f

stop:
	docker stop video-processing-service

sh:
	docker exec -it video-processing-service sh