# S3 CORS configuration
```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "http://localhost:8080"
        ],
        "ExposeHeaders": [
            "ETag"
        ]
    }
]
```

# Flow
```mermaid
sequenceDiagram
    participant Client as Browser
    participant Server as Go Server
    participant S3 as AWS S3

    Client->>Server: Select file and initiate upload
    Server->>S3: CreateMultipartUpload
    S3-->>Server: Return UploadId
    Server-->>Client: Return UploadId

    loop For each part
        Client->>Server: Request presigned URL
        Server->>S3: PresignUploadPart
        S3-->>Server: Return presigned URL
        Server-->>Client: Return presigned URL
        Client->>S3: Upload part using presigned URL
        S3-->>Client: Return ETag for part
        Client->>Client: Store ETag and PartNumber
    end

    Client->>Server: Complete multipart upload (with ETags and PartNumbers)
    Server->>S3: CompleteMultipartUpload
    S3-->>Server: Confirm completion
    Server-->>Client: Confirm upload success
```

# Etag
- etag from S3 is md5(blob)
- putObject returns etag
- client-side calculated md5 is compared with etag from S3
- if they are different, the part is re-uploaded
- at completeMultipartUpload, the etags are verified again
- if any etag is different, the whole multipart upload is aborted and re-uploaded