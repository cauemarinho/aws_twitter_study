CREATE EXTERNAL TABLE IF NOT EXISTS athenacaue.tweet (
  `created_at` string,
  `twitter_id` string,
  `text` string,
  `userid` string,
  `username` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://s3datacaue/'
TBLPROPERTIES ('has_encrypted_data'='false');