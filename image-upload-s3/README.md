# AdvancedNodeStarter

Starting project for a course on Advanced Node @ Udemy

### Installation

- Run `npm install` in the root of the project to install the server's dependencies
- Change into the client directory and run `npm install --legacy-peer-deps`
- Change back into the root of the project and run `npm run dev` to start application

**Important** - the Mongo Atlas database credentials provided in `dev.js` are read only. If you attempt to login without using your own connection string (covered in the course) you will get the following error `[0] MongoError: user is not allowed to do action [insert] on [advnode.users]`

### S3 setup
- Step 1: Create bucket (like a folder) in S3
- Use IAM: create user credentials with limited access scope (only to S3)
  - Policy: `image-upload-app-admin-policy` describe what/who can read/write bucket `image-upload-app`
    - choose service s3
    - allow all actions
    - resources
      - bucket: `image-upload-app`
      - object: `image-upload-app/*` (all objects in the bucket)
  - User: `image-upload-app-admin`
    - Attach policy `image-upload-app-admin-policy`
- Manage:
  - https://658269753957.signin.aws.amazon.com/console
- CORS error uploading image to S3
  - S3 bucket > Permissions > CORS configuration
  - Add CORS configuration
```js
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    },
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT"
        ],
        "AllowedOrigins": [
            "http://localhost:3000"
        ],
        "ExposeHeaders": []
    }
]
```
  - Save
- Access uploaded image: bucket > permissions > policy
```json
{
    "Version": "2012-10-17",
    "Id": "Policy1707235877663",
    "Statement": [
        {
            "Sid": "Stmt1707235867533",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::image-upload-app/*"
        }
    ]
}
```
- Best practise
  - Store the path of the image in the database: `${user.id}/${filename}`
  - Link can be dynamically generated: `https://s3.amazonaws.com/image-upload-app/${user.id}/${filename}`