# CS 410 Course Project
# Sentiment Analysis of twitter samples using Amazon Comprehend
# This will use the downloaded "twitter_samples" corpus of NLTK. The twitter samples contain labeled positive and
# negative tweets. Amazon Comprehend API will be used to do sentiment classification of the testing portion of
# this dataset. The same testing portion will be used to do sentiment analysis using NLTK and the results will
# be compared.

import boto3
import json
import sys

# Total, positive, negative, neutral and mixed sentiment tweet counts
total_count = 0
correct_positive_count = 0
correct_negative_count = 0
neutral_count = 0
mixed_count = 0
other_counts = 0

def invoke_sentiment_analysis_lambda(tweets_dataset):
    # Declare globals
    global total_count, correct_positive_count, correct_negative_count
    global neutral_count, mixed_count, other_counts
    for item in tweets_dataset:
        total_count += 1
        lambda_payload = {"tweet_text":item,"language_code":"en"}
        response = lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:765679423646:function:sentimentAnalysisLambda',
                     InvocationType='RequestResponse',
                     Payload=json.dumps(lambda_payload))
        resp_data = response['Payload'].read()
        resp_obj = json.loads(resp_data)
        sentiment_value = resp_obj['body']['Sentiment']
        # print(sentiment_value)
        if sentiment_value == "POSITIVE":
            correct_positive_count += 1
        elif sentiment_value == "NEGATIVE":
            correct_negative_count += 1
        elif sentiment_value == "NEUTRAL":
            neutral_count += 1
        elif sentiment_value == "MIXED":
            mixed_count += 1
        else:
            other_counts += 1
    return

######## Main Program ########
if __name__ == "__main__":

    # Check if input argument is present
    num_args = len(sys.argv)
    # Exit is num args != 2
    if num_args != 2:
        print("Usage: python3 sentiment_analysis_amazon_comprehend.py <1 (keep smileys) or 2 (remove smileys)>")
        print("Example: python3 sentiment_analysis_amazon_comprehend.py 1")
        sys.exit()

    # Get the remove smiley flag
    if sys.argv[1] == '1':
        remove_smileys = False
    elif sys.argv[1] == '2':
        remove_smileys = True
    else:
        print("Invalid argument!")
        sys.exit()

    # Get the AWS Lambda client which will invoke the AWS Lambda function
    lambda_client = boto3.client('lambda', region_name='us-east-1', aws_access_key_id='',
        aws_secret_access_key='')

    # Open file which contains positive and negative tweets
    if remove_smileys:
        positive_tweets_file = open('../../data/amazon_comprehend/amz_positive_tweets_smiley_removed.txt', 'r')
        negative_tweets_file = open('../../data/amazon_comprehend/amz_negative_tweets_smiley_removed.txt', 'r')
    else:
        positive_tweets_file = open('../../data/amazon_comprehend/amz_positive_tweets.txt', 'r')
        negative_tweets_file = open('../../data/amazon_comprehend/amz_negative_tweets.txt', 'r')

    # Read files into tweets datasets
    positive_tweets_dataset = positive_tweets_file.readlines()
    negative_tweets_dataset = negative_tweets_file.readlines()

    # Invoke AWS lambda function for classifying positive tweets dataset
    invoke_sentiment_analysis_lambda(positive_tweets_dataset)
    # Invoke AWS lambda function for classifying positive tweets dataset
    invoke_sentiment_analysis_lambda(negative_tweets_dataset)

    # Calculate accuracy and print counts
    testing_accuracy = (correct_positive_count + correct_negative_count) / total_count
    print("Correct positive count: ", correct_positive_count)
    print("Correct negative count: ", correct_negative_count)
    print("Neutral count: ", neutral_count)
    print("Mixed count: ", mixed_count)
    print("Other count: ", other_counts)
    print("Total count: ", total_count)
    print("Accuracy: ", testing_accuracy)

######## End of Main Program ########
