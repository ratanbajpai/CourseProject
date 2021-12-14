# CS 410 Course Project
# Sentiment Analysis of twitter samples using NLTK
# This will use the downloaded "twitter_samples" corpus of NLTK. The twitter samples contain labeled positive and
# negative tweets, which will be used to train a model. Once the model is trained, the sentiment analysis task will
# be performed on the test data.

# This part of the code is guided by an online tutorial which was suitably
# modified to fit the needs and improve processing.
# (https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk)

# NLTK, twitter_samples and other imports
import nltk
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import classify
from nltk import NaiveBayesClassifier
import re, string
import random
import sys

# Flag for ignoring or keeping smileys to classify tweets
remove_smileys = True

# Utility function to remove puntuation, urls and twitter handles from the tokenized tweet text
# After the tweet tokens are cleaned, they are lemmatized and the lemmatized list is returned
def clean_and_lemmatize_tokens(tweet_tokens, word_lemmatizer, stop_words = ()):
    lemmatized_tokens = []
    # Use pos_tag function to attach part of speech to the tokens.
    # For each token and POS tag...
    for token, tag in pos_tag(tweet_tokens):
        # Lowercase all the letters
        token = token.lower()
        # Remove twitter handles
        token = re.sub("@[A-Za-z0-9_]+","", token)
        # Remove hashtags
        token = re.sub("#[A-Za-z0-9_]+","", token)
        # Remove urls
        token = re.sub(r"http\S+", "", token)
        token = re.sub(r"www.\S+", "", token)
        # If the remove smiley flag is set to true, remove ":)" and ":("
        # characters
        if remove_smileys:
            # Remove puntuations
            token = re.sub('[()!?]', "", token)
            token = re.sub('\[.*?\]', "", token)
            # Remove alpha-numeric characters
            token = re.sub("[^a-z0-9]", "", token)
        # Remove stop words
        if len(token) > 0 and token not in stop_words:
            # Lemmatize the cleaned token
            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            # Use the passed in word lemmatizer
            token = word_lemmatizer.lemmatize(token, pos)
            # Append to the lemmatized token list
            lemmatized_tokens.append(token)
    return lemmatized_tokens

# This function takes a list of cleaned and lemmatized tokens and adds "True" for each
# feature to be included in the feature list. It also labels the data as "Positive" or
# "Negative"
def prep_model_data(lemmatized_tokens_list, label):
    # Initialize a list of training or testing data. This will be a list
    # of tuples where first element is a dictionary containing featues and
    # second element is the label, whether the tweet sentiment is "Positive" or
    # "Negative". Each element of the list will look as follows:
    # ({feature1: True, feature2: True,....}, "Positive"). This is the format
    # in which the classifier takes the input data.
    classifier_input_data_list = []
    for tweet_tokens in lemmatized_tokens_list:
        # Initialize the dictionary that will have features and include flag
        input_features = {}
        for token in tweet_tokens:
            # We will include all tokens as input_features and mark them True
            input_features[token] = "True"
        # Create a tuple of the above dictionary and the given label
        input_features_with_label = (input_features, label)
        # Add this input data to the list
        classifier_input_data_list.append(input_features_with_label)
    # Return the classifier input data list
    return classifier_input_data_list



######## Main Program ########
if __name__ == "__main__":

    # Check if input argument is present
    num_args = len(sys.argv)
    # Exit is num args != 2
    if num_args != 2:
        print("Usage: python3 sentiment_analysis_nltk.py <1 (keep smileys) or 2 (remove smileys)>")
        print("Example: python3 sentiment_analysis_nltk.py 1")
        sys.exit()

    # Get the remove smiley flag
    if sys.argv[1] == '1':
        remove_smileys = False
    elif sys.argv[1] == '2':
        remove_smileys = True
    else:
        print("Invalid argument!")
        sys.exit()

    # Setup variables for positive, negative and neutral tweets. Using the strings
    # method of imported "twitter_samples" corpus, get text data in tweets
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    # Tokenize positive and negative tweets
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # Remove links, twitter handles, hashtags, puntuations etc. and lemmatize
    # Get stopwords list
    stop_words = stopwords.words('english')
    # Get word lemmatizer
    word_lemmatizer = WordNetLemmatizer()
    # Initialize output lists
    positive_lemmatized_tokens_list = []
    negative_lemmatized_tokens_list = []
    # Get lemmatized positive tokens list
    for tokens in positive_tweet_tokens:
        positive_lemmatized_tokens_list.append(clean_and_lemmatize_tokens(tokens, word_lemmatizer, stop_words))
    # Get lemmatized native tokens list
    for tokens in negative_tweet_tokens:
        negative_lemmatized_tokens_list.append(clean_and_lemmatize_tokens(tokens, word_lemmatizer, stop_words))

    # This step creates a list of tuple where each tuple contains a dictionary of
    # input features and a label. We create training data for a set of positive
    # and negative tweets. Each dictionary contains features as key and a include
    # flag (True, False to include feature or not). The label indicates if the
    # tweet sentiment is positive or negative (labeled data).
    positive_labeled_dataset = prep_model_data(positive_lemmatized_tokens_list, "Positive")
    negative_labeled_dataset = prep_model_data(negative_lemmatized_tokens_list, "Negative")

    # We will use the first 3750 tweets data from each set to total of 7500 items for training data
    training_dataset = positive_labeled_dataset[:3750] + negative_labeled_dataset[:3750]
    # Shuffle training data to remove any bias
    random.shuffle(training_dataset)
    # Use remaining 1250 items from each set as testing dataset
    testing_dataset = positive_labeled_dataset[3750:] + negative_labeled_dataset[3750:]
    # Shuffle testing data to remove any bias
    random.shuffle(testing_dataset)

    # Train the Naive Bayes Classifier
    nb_classifier = NaiveBayesClassifier.train(training_dataset)

    # Now test the trained model accuracy on testing dataset
    testing_accuracy = classify.accuracy(nb_classifier, testing_dataset)
    print("Testing accuracy is:", testing_accuracy)

    # Top 20 most informative features
    nb_classifier.show_most_informative_features(20)

######## End of Main Program ########
