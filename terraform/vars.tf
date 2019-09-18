variable "aws_region" {
    default = "us-east-1"
}

variable "bucket_schema" {
    default = "s3schemacaue"
}

variable "bucket_data" {
    default = "s3datacaue"
}

variable "athena_database" {
    default = "athenacaue"
}

variable "dynamo_name" {
    default = "user_tweet"
}

variable "stream_name" {
    default = "streamcaue"
}

variable "firehose_name" {
    default = "firehosecaue"
}

variable "tag_name" {
    default = "twitter"
}