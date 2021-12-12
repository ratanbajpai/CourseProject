# CourseProject

This repository contains the final project source code and documentation for CS410. In this project we are doing sentiment analysis for the "Twitter Samples" dataset from NLTK Corpora. We are using two approaches and then comparing results from both approaches. One approach is to use Amazon Comprehend which is a high level NLP API from Amazon. Another approach is to use Natural Language Toolkit which is a python library for NLP. It provides low level flexibility to train models based on different classifiers.

## Amazon Comprehend

The source for Amazon Comprehend is in src/amazon_comprehend and data is in data/amazon_comprehend. The video on how to setup and run the Amazon Comprehend part in in the doc folder. There is a setup and run presentation (pdf) in the doc directory which lists the installation steps for various components to run this part. The slides contain a step which is missing in the video and that is on how to point to the correct AWS Lambda using it's arn id.

## Natural Language Toolkit (NLTK)

Similar to Amazon Comprehend the source, data, setup & run video, and presentation for NLTK are in src/nltk, data/nltk and the doc folder. The setup for NLTK is relatively easier.

## Comparing Both Approaches

The description of the software as well as detailed steps in each of the above approaches are described in the ProjectFinalReport.pdf which is in the doc folder. This report also contains the sentiment analysis results and conclusions for both approaches. Since the setup for running the NLTK part is fairly easy, it's recommended to run this part and see the results. The setup for Amazon Comprehend is more involved and may also cost money if the free AWS tier is not available. It's therefore recommended to see how this approach works and the results of a run in the setup video itself.

