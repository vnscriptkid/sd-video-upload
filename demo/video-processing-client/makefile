PROJECT_ID=video-processing-17e6f
REGION=asia-southeast1
REPO_NAME=video-processing-client-repo
IMAGE_NAME=video-processing-client-service

repo_create:
	gcloud artifacts repositories create $(REPO_NAME) \
		--repository-format=docker \
		--location=$(REGION) \
		--description="Docker repository for youtube web client"

build_prod:
	docker build --platform linux/amd64 -t $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME) .

repo_push:
	docker push $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME)

cloud_run:
	gcloud run deploy $(IMAGE_NAME) --image $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME) \
		--region=$(REGION) \
		--platform managed \
		--timeout=3600 \
		--memory=2Gi \
		--cpu=1 \
		--min-instances=0 \
		--max-instances=1

deploy: build_prod repo_push cloud_run