{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
    ],
    "Resource": [
        "arn:aws:s3:::my-etl-bucket",
        "arn:aws:s3:::my-etl-bucket/*"
    ]
}