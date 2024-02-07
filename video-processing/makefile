### define the project id as "abc"
PROJECT_ID=video-processing-17e6f
REGION=asia-southeast1
REPO_NAME=video-processing-repo
IMAGE_NAME=video-processing-service
SERVICE_URL=https://video-processing-service-nldiin3tva-as.a.run.app
TOPIC_NAME=video-processing-topic
SUBSCRIPTION_NAME=video-processing-sub
BUCKET_RAW_NAME=video-raw-bucket
BUCKET_PROCESSED_NAME=video-processed-bucket

build:
	docker build --platform linux/amd64 -f Dockerfile.local -t video-processing-service .

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

echo:
	echo $(PROJECT_ID)

#### Deploy to Cloud Run
## Step 0
repo_auth:
	gcloud auth configure-docker $(REGION)-docker.pkg.dev

## Step 1
# --platform linux/amd64: if you are using mac
build_prod:
	docker build --platform linux/amd64 -t $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME) .
## Step 2
repo_push:
	docker push $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME)

## Step 3: Notice Service URL
cloud_run:
	gcloud run deploy $(IMAGE_NAME) --image $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(IMAGE_NAME) \
		--region=$(REGION) \
		--platform managed \
		--timeout=3600 \
		--memory=2Gi \
		--cpu=1 \
		--min-instances=0 \
		--max-instances=1 \
		--ingress=internal

## Enable svc
enable_svc: # cloud run, artifact registry
	gcloud services enable run.googleapis.com 
	gcloud services enable artifactregistry.googleapis.com

## Gcloud pubsub
topic_create:
	gcloud pubsub topics create $(TOPIC_NAME)

sub_create:
	gcloud pubsub subscriptions create $(SUBSCRIPTION_NAME) \
		--topic=$(TOPIC_NAME) \
		--push-endpoint=$(SERVICE_URL) \
		--ack-deadline=600

sub_delete:
	gcloud pubsub subscriptions delete $(SUBSCRIPTION_NAME)

## Gcloud storage bucket
# --pap=enforced: set the bucket to be private
bucket_raw_create:
	gsutil mb -l $(REGION) --pap=enforced gs://$(BUCKET_RAW_NAME)

bucket_processed_create:
	gsutil mb -l $(REGION) gs://$(BUCKET_PROCESSED_NAME)

# -e OBJECT_FINALIZE: trigger when a new object is created
bucket_raw_notif_create:
	gsutil notification create -t $(TOPIC_NAME) -f json -e OBJECT_FINALIZE gs://$(BUCKET_RAW_NAME)