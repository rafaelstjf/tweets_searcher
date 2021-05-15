import tweepy, argparse, io, json, os
from json import encoder

def get_tweets(symptoms, keywords, query, lang):
    max_count = 1000
    print("--------------------------------------")
    print("\t\tDownloading tweets")
    print("Query: " + query)
    print("keywords: {}" .format(keywords))
    print("Symptoms: {}" .format(symptoms))
    print("Maximum number of tweets for each keyword: {}" .format(max_count))
    print("Language: " + lang)
    print("--------------------------------------")
    # empty list to store parsed tweets
    tweets = []
    # call twitter api to fetch tweets
    if len(symptoms) == 0:
        for kw in keywords:
            print("Downloading tweets for the keyword \"{}\"..." .format(kw))
            try:
                tweets +=tweepy.Cursor(api.search, lang=lang, q=(query + " " + kw + " " + s), tweet_mode='extended').items(max_count)
                print("* Done")
            except:
                print("* Failed")
    else:
        for s in symptoms:
            for kw in keywords:
                print("Downloading tweets for the keyword \"{}\", looking for symptom \"{}\"..." .format(kw, s),)
                try:
                    tweets +=tweepy.Cursor(api.search, lang=lang, q=(query + " " + kw + " " + s), tweet_mode='extended').items(max_count)
                    print("* Done")
                except:
                    print("* Failed")
    return tweets

def save_tweets(out_filename, tweets):
    saved = {}
    print("Saving tweets in the output file")
    try:
        out_file = open(out_filename, 'w+', encoding='utf8')
        for tw in tweets:
            if tw.id not in saved.keys():
                tw_json = tw._json
                tw_filtered = {}
                tw_filtered["created_at"] = tw_json["created_at"]
                tw_filtered["id"] = tw_json["id"]
                tw_filtered["full_text"] = tw_json["full_text"]
                tw_filtered["lang"] = tw_json["lang"]

                try:
                    out_file.write(json.dumps(tw_filtered, ensure_ascii=False))
                    out_file.write('\n')
                    saved[tw.id] = True #guarantee that there aren't any repeated ids
                except:
                    print("Error while saving the following tweet")
                    print(type(tw_filtered["created_at"]))
                    print(type(tw_filtered["id"]))
                    print(type(tw_filtered["full_text"]))
                    print(type(tw_filtered["lang"]))
        print("Tweets saved!")
    except IOError:
        print("Output file could not be created!")


def create_csv(in_filename, out_filename, symptoms, sep=';'):
    try:
        with open(in_filename, 'r',  encoding='utf-8') as json_file:
            json_list = list(json_file)
            data = []
            buffer = ""
            buffer = "class" + sep + "id" + sep + "text" + sep + "created_at" + sep + "language"
            for s in symptoms:
                buffer += sep + s[0]
            buffer+='\n'
            for json_str in json_list:
                data = json.loads(json_str)
                buffer+= "?" + sep
                if "text" in data.keys():            
                    buffer+= str(data["id"]) + sep + "\"" + data["text"].replace("\n", " ").replace("\"", "\"\"") + "\"" + sep + data["created_at"] + sep + data["lang"]
                    text =data["text"].lower()
                    for s in symptoms:
                        val = sep + '0'
                        if text.count(s) > 0:
                            val= sep + '1'
                        else:
                            buffer+= val
                    buffer+='\n'
                else:
                    buffer+=str(data["id"]) + sep + "\"" + data["full_text"].replace("\n", " ").replace("\"", "\"\"") + "\"" + sep + data["created_at"] + sep + data["lang"]
                    text =data["full_text"].lower()
                    for s in symptoms:
                        val = sep + '0'
                        if text.count(i) > 0:
                            val= sep + '1'
                        buffer+= val
                    buffer+='\n'
        json_file.close()
        with open(out_filename, 'w+', encoding='utf-8') as out:
            out.write(buffer)
            out.close()
    except:
        print("Error while creating the csv")

#get the environment variables
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')


def main():
    #load and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', required=True, help='Name of the configuration file')
    parser.add_argument('-co', '--convert_to_csv', required = False, help="Converts the jsonl file to csv and save in the informed output")
    args = parser.parse_args()

    #load configuration file

    try:
        json_file = open(args.config_file)
        configs = json.load(json_file)
    except:
        print("Error loading the configuration file! Exiting...")
        exit(1)

    #Authenticate the account
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=set([503]))
    #Parameters
    tweets = get_tweets(configs["symptoms"], configs["keywords"], configs["query"] + " " + configs["blacklist"], configs["language"])
    save_tweets(configs["output_file"], tweets)
    if(args.convert_to_csv != ""):
      create_csv(configs["output_file"], args.convert_to_csv, configs["symptoms"])  


if __name__ == "__main__":
    main()