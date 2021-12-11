# CS 410 Course Project
# This is the lambda function that runs in AWS and invokes the Amazon
# Comprehend APIs for sentiment analysis of twitter_samples.

import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    # This part of code is needed if the twitter_samples data file
    # is stored in an S3 bucket
    # s3 = boto3.client("s3")
    # s3_bucket = "cs410-project-twitter-samples"
    # file_key = "TwitterSamples/test_negative_tweet.txt"
    # tweet_object = s3.get_object(Bucket = s3_bucket, Key = file_key)
    # tweet_text = str(tweet_object['Body'].read())

    # Get the tweet text from the incoming request
    tweet_text = event['tweet_text']
    # print(tweet_text)
    amz_comprehend = boto3.client("comprehend")
    sentiment_resp = amz_comprehend.detect_sentiment(Text = tweet_text, LanguageCode = "en")
    # print(sentiment_resp)
    return {
        'statusCode': 200,
        'body': sentiment_resp
    }
