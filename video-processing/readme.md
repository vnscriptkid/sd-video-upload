# video processing svc

## libs
- fluent-ffmpeg
- https://ffmpeg.org/download.html
- @google-cloud/storage

## docker
- Take advantage of docker layer caching by copying package.json and package-lock.json first, then running npm install, then copying the rest of the files.
```Dockerfile
COPY package*.json ./
RUN npm install
COPY . .
```

- Why Docker multi-stage build?
