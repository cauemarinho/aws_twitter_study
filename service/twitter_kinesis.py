import boto3
import tweepy
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
access_token_key = config['twitter']['access_token_key']
access_token_secret = config['twitter']['access_token_secret']
region = config['aws']['region']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

my_stream_name = 'streamcaue'
hashtag_search = '#LOL'
hashtag_replace = hashtag_search.replace('#', '')
kinesis_client = boto3.client('kinesis', region_name=region)


class KinesisStreamProducer(tweepy.StreamListener):

    def __init__(self, kinesis_client):
        self.kinesis_client = kinesis_client

    @staticmethod
    def schema_json(created_at, twitter_id, text, user_id, user_name):
        data = {
            'created_at': str(created_at),
            'twitter_id': str(twitter_id),
            'text': str(text),
            'userid': str(user_id),
            'username': str(user_name)
        }
        return data

    @staticmethod
    def put_to_stream(data):
        kinesis_client.put_record(
            StreamName=my_stream_name,
            Data=json.dumps(data) + '\n',
            PartitionKey=hashtag_replace)

    def on_data(self, data):
        created_at = json.loads(data)['created_at']
        twitter_id = json.loads(data)['id']
        text = json.loads(data)['text']
        user_id = json.loads(data)['user']['id']
        user_name = json.loads(data)['user']['name']
        tweet = self.schema_json(created_at=created_at, twitter_id=twitter_id, text=text, user_id=user_id, user_name=user_name)
        self.put_to_stream(tweet)
        print("Publishing record to the stream: ", tweet , '\n')
        return True

    def on_error(self, status):
        print("Error: " + str(status))


def main():
    mylistener = KinesisStreamProducer(kinesis_client)
    myStream = tweepy.Stream(auth=auth, listener=mylistener)
    myStream.filter(track=['#LOL'])


if __name__ == "__main__":
    main()



