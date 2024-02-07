## firebase functions
- npm install -g firebase-tools
- firebase login
- firebase init functions
- npm install firebase-functions@latest firebase-admin@latest
- npm run serve
- firebase deploy --only functions

## permission
- get svc account of function `generateUploadUrl`
- grant permission to svc account to upload file to bucket `video-raw-bucket`
  - go to bucket `video-raw-bucket`
  - permission > grant access: cloud storage > storage object admin
- grant permission to svc account create token
  - go to project > IAM & admin > service account of function `generateUploadUrl` 
  - add role: service account token creator