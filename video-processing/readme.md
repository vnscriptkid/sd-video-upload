# video processing svc

## libs
- fluent-ffmpeg
- https://ffmpeg.org/download.html
- @google-cloud/storage
- firebase-admin

## docker
- Take advantage of docker layer caching by copying package.json and package-lock.json first, then running npm install, then copying the rest of the files.
```Dockerfile
COPY package*.json ./
RUN npm install
COPY . .
```

- Why Docker multi-stage build?

## gcloud
- https://console.cloud.google.com/home/dashboard?hl=vi&project=video-processing-17e6f
- gcloud auth login
- gcloud config set project video-processing-17e6f
- Enable svc: Artifact Registry API
  - gcloud services enable artifactregistry.googleapis.com
- Svc locations: https://cloud.google.com/about/locations#asia-pacific
  - asia-southeast1
- Create repo
```bash
gcloud artifacts repositories create video-processing-repo \
  --repository-format=docker \
  --location=asia-southeast1 \
  --description="Docker repository for video processing service"
```
- Service URL: https://video-processing-service-nldiin3tva-as.a.run.app