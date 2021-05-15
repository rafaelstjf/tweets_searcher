## Context 

I created this script to download search for tweets about symptoms in the context of covid. It does a "cartesian product" of the symptoms and keywords, all of that using the Tweepy API. It's a very simple script for personal use, but feel free to adapt it to your case of study and use as you wish.

### Requirements

* Tweepy library

* The twitter's tokens as environment variables: CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN and ACCESS_SECRET

  ### How to use

  The script uses as input a json file that contains all the needed parameters

  ```json
  {
      "output_file": "file.jsonl",
      "keywords": ["covid", "corona", "c19"],
      "symptoms": ["symptom1", "symptom2", "symptom_n"],
      "blacklist": "-death -anxiety",
      "query": "-filter:retweets -filter:images",
      "language": "pt"
  }
  ```

  The script is called as follow:

  ```python
  python downloader.py -c configuration.json
  ```

  The script stores the tweets in a jsonl file, but you can also use the argument ``` -co file.csv``` to convert it to csv.

