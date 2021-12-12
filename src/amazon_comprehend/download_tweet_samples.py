# CS 410 Course Project
# This utility script downloads the twitter_samples data which is stored in
# NLTK to flat files so that it can become input for Amazon Comprehend

import nltk
from nltk.corpus import twitter_samples
import re

positive_emojis = [':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3']

negative_emojis = [':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';(']

def save_tweets_data(tweets_data, file_name, remove_smileys):
        with open(file_name, 'w') as f:
            # We just need to save the last 1250 rows as test data
            for i in range(3750, len(tweets_data)):
                token = tweets_data[i]
                # If we don't need smileys, remove them
                if remove_smileys:
                    # Remove puntuations
                    for item in positive_emojis:
                        token = token.replace(item, '')
                    for item in negative_emojis:
                        token = token.replace(item, '')
                    # token = re.sub('[()!?]', "", token)
                    # token = re.sub('\[.*?\]', "", token)
                    # Remove alpha-numeric characters
                    # token = re.sub("[^a-z0-9]", "", token)
                f.write("%s\n" % token)


######## MAIN PROGRAM ########

if __name__ == "__main__":

    # Setup variables for positive and negative tweets. The strings method
    # just gets the tweet text for all the twitter_samples data.
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    # Store the tweets data in separate files for testing with Amazon Comprehend
    # Positive tweets with smileys
    save_tweets_data(positive_tweets, '../../data/amazon_comprehend/amz_positive_tweets.txt', False)
    # Positive tweets without smileys
    save_tweets_data(positive_tweets, '../../data/amazon_comprehend/amz_adj_positive_tweets.txt', True)
    # Negative tweets with smileys
    save_tweets_data(negative_tweets, '../../data/amazon_comprehend/amz_negative_tweets.txt', False)
    # Negative tweets without smileys
    save_tweets_data(negative_tweets, '../../data/amazon_comprehend/amz_adj_negative_tweets.txt', True)

######## END MAIN PROGRAM ########
