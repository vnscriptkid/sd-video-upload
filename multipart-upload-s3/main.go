package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

var s3Client *s3.Client
var s3BucketName string
var s3Region string
var s3AccessKeyID string
var s3SecretAccessKey string

func initS3() {
	// Load .env file
	if err := godotenv.Load(); err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}

	s3BucketName = os.Getenv("BUCKET_NAME")
	s3Region = os.Getenv("AWS_REGION")
	s3AccessKeyID = os.Getenv("AWS_ACCESS_KEY_ID")
	s3SecretAccessKey = os.Getenv("AWS_SECRET_ACCESS_KEY")

	cfg, err := config.LoadDefaultConfig(context.TODO(),
		config.WithRegion(s3Region),
		config.WithCredentialsProvider(credentials.NewStaticCredentialsProvider(
			s3AccessKeyID,
			s3SecretAccessKey,
			"",
		)),
	)
	if err != nil {
		log.Fatalf("unable to load SDK config, %v", err)
	}

	s3Client = s3.NewFromConfig(cfg)
}

func main() {
	r := gin.Default()

	initS3()

	r.StaticFile("/", "./index.html")
	r.POST("/initiate-multipart-upload", initiateMultipartUpload)
	r.POST("/generate-presigned-url", generatePresignedURL)
	r.POST("/complete-multipart-upload", completeMultipartUpload)

	r.Run(":8080")
}

func initiateMultipartUpload(c *gin.Context) {
	key := "uploads/" + c.Query("filename")

	input := &s3.CreateMultipartUploadInput{
		Bucket: aws.String(s3BucketName),
		Key:    aws.String(key),
	}

	result, err := s3Client.CreateMultipartUpload(context.TODO(), input)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"uploadID": *result.UploadId,
	})
}

func generatePresignedURL(c *gin.Context) {
	key := "uploads/" + c.Query("filename")
	uploadID := c.Query("uploadId")
	// parse part number from query string and convert it to int 32
	partNumber, err := strconv.ParseInt(c.Query("partNumber"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	partNumber32 := int32(partNumber)

	presignClient := s3.NewPresignClient(s3Client)

	req, err := presignClient.PresignUploadPart(context.TODO(), &s3.UploadPartInput{
		Bucket:     aws.String(s3BucketName),
		Key:        aws.String(key),
		UploadId:   aws.String(uploadID),
		PartNumber: &partNumber32,
	}, s3.WithPresignExpires(15*time.Minute))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"url": req.URL,
	})
}

func completeMultipartUpload(c *gin.Context) {
	key := "uploads/" + c.Query("filename")
	uploadID := c.Query("uploadId")

	var completedParts []types.CompletedPart
	if err := c.ShouldBindJSON(&completedParts); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	completeInput := &s3.CompleteMultipartUploadInput{
		Bucket:   aws.String(s3BucketName),
		Key:      aws.String(key),
		UploadId: aws.String(uploadID),
		MultipartUpload: &types.CompletedMultipartUpload{
			Parts: completedParts,
		},
	}

	_, err := s3Client.CompleteMultipartUpload(context.TODO(), completeInput)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Upload completed successfully",
	})
}
