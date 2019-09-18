provider "aws" {
  region = "${var.aws_region}"
}

resource "aws_s3_bucket" "tweets" {
  bucket = "${var.bucket_data}"
  acl    = "private"
  tags = {
    Name = "${var.tag_name}"
  }
}
resource "aws_s3_bucket" "tweets2" {
  bucket = "${var.bucket_schema}"
  acl    = "private"
  tags = {
    Name = "${var.tag_name}"
  }
}

resource "aws_athena_database" "tweet" {
  name   = "${var.athena_database}"
  bucket = "${aws_s3_bucket.tweets2.bucket}/query/"
}

resource "aws_kinesis_stream" "tweets" {
  name             = "${var.stream_name}"
  shard_count      = 1
  retention_period = 48
  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
  tags = {
    Name = "${var.tag_name}"
  }
}

resource "aws_dynamodb_table" "tweets" {
    name = "${var.dynamo_name}"
    read_capacity = 10
    write_capacity = 10
    hash_key = "user"

    attribute {
        name = "user"
        type = "N"
    }
}


