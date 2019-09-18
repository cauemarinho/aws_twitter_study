import boto3
import json
import configparser
import time
from decimal import Decimal

config = configparser.ConfigParser()
config.read('config.ini')
region = config['aws']['region']

my_stream_name = 'streamcaue'
table = 'user_tweet'

dynamodb = boto3.resource('dynamodb', region_name=region)
kinesis_client = boto3.client('kinesis', region_name=region)
table = dynamodb.Table(table)

response = kinesis_client.describe_stream(StreamName=my_stream_name)
my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']
shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                   ShardId=my_shard_id,
                                                   ShardIteratorType='LATEST')

my_shard_iterator = shard_iterator['ShardIterator']
record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                             Limit=2)

while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                 Limit=2)

    if len(record_response['Records']) > 0:
        tweet = json.loads(record_response['Records'][0]['Data'].decode('utf-8'))
        user = tweet['userid']
        userDecimal = Decimal(user)

        response = table.get_item(
            Key={
                    'user': Decimal(user)
                }
            )

        if 'Item' not in response:
            response = table.put_item(
                Item={
                        'user': userDecimal,
                        'count': 1
                    }
                )
            print('Insert DynamoDB: User = ', user)
        else:
            count = response['Item']['count']+1
            response = table.put_item(
                Item={
                        'user': userDecimal,
                        'count': count
                    }
                )
            print('Update DynamoDB: User = ', user, ', Count = ', count)

    time.sleep(2)
