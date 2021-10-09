import tweepy
import json
import requests
from time import sleep

try: 
    config_file = open("config.json", "r")
    config = json.loads(config_file.read())
except Exception as err:
    print(f"An error occurred while attempting to read config.json\n{err}\n\n")
    exit()

def shutdown(msg:str):
    print(msg)
    sendMobilePush("Listener stopped!", msg)
    exit()

def sendMobilePush(title:str, body:str) -> bool:
    r = requests.post("https://api.pushbullet.com/v2/pushes",headers={"Access-Token":config["sender"]["push_bullet_token"]},data={"type": "note","title": title, "body": body})

def printError(err,console_msg:str,is_critical:bool,notify_mobile:bool,mobile_body:str) -> None:
    print(f"{console_msg}\n{err}")
    if notify_mobile == True and config["sender"]["msg_on_error"] == True:
        sendMobilePush("Listener error!", mobile_body)
    if is_critical == True:
        shutdown("A critical error has occurred and the program has been shut down\n")
    
def fetchTweets(count:int,include_rts:bool,exclude_replies:bool,force_to_lower:bool) -> list:
    try:
        query = api.user_timeline(screen_name=config["finder"]["user_handle"],count=count,exclude_replies=exclude_replies,include_rts=include_rts,tweet_mode="extended")
    except Exception as err:
        printError(err, "Failed to fetch tweets, will try again on the next iteration!", False, True, "Failed to fetch tweets, will try again on the next iteration!")
    else:
        tweet_list = []
        for tweet in query:
            tweet_content = tweet.full_text
            if force_to_lower == True:
                tweet_content = tweet_content.lower()
            tweet_list.append(tweet_content)
        return tweet_list
        
try:
    auth = tweepy.OAuthHandler(config["key"], config["secret"])
    auth.set_access_token(config["access"]["token"], config["access"]["secret"])
    api = tweepy.API(auth)
except Exception as err:
    printError(err, "An issue occurred while attempting to authenticate through the twitter API.", True, False)

history = []
if config["sender"]["msg_on_startup"] == True:
    sendMobilePush("Listener started!", "Listener successfully started. You will be notified when the keyword is mentioned.")
# Create an archive of tweets if the user doesn't want to be notified of tweets containing a keyword in the past
if config["finder"]["ignore_past_tweets"] == False:
    tweet_list = fetchTweets(config["finder"]["initial_scan_count"],False,config["finder"]["ignore_replies"],True)
    for status in tweet_list:
        if status not in history:
            history.append(status)

while True:
    try:
        # Check the length of the history of tweets. If tweet amount exceeds memory in config,
        # we remove the oldest tweets in the list
        while len(history) > config["finder"]["memory"]:
            history.pop(len(history) - 1)
        # Fetch recent tweets
        recent_log = []
        recent_log = fetchTweets(config["finder"]["search_count"],False,config["finder"]["ignore_replies"],True)
        for tweet in recent_log:
            if tweet not in history:
                # Check if the tweet contains the keyword, if it does we execute the output here
                if config["finder"]["keyword"] in tweet:
                    sendMobilePush(config["sender"]["title"],config["sender"]["body"])
                    print(f"Found keyword \"{config['finder']['keyword']}\" in tweet!\n> {tweet}")
                # Add the tweet to the history variable, since the tweet does not exist here, and we need
                # to archive the tweet regardless of if it contains our keyword
                history.insert(0, tweet)
        # Puts the finder to sleep for X minutes
        sleep(config["finder"]["search_frequency"] * 60)
    except KeyboardInterrupt:
        sendMobilePush("Listener stopped!", "Listener was manually stopped through the console")