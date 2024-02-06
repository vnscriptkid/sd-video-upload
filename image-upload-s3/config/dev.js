module.exports = {
  googleClientID:
    '70265989829-0t7m7ce5crs6scqd3t0t6g7pv83ncaii.apps.googleusercontent.com',
  googleClientSecret: '8mkniDQOqacXtlRD3gA4n2az',
  mongoURI: process.env.MONGO_URI,
  cookieKey: '123123123',
  redisUrl: process.env.REDIS_URL,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  s3Bucket: 'image-upload-app'
};
