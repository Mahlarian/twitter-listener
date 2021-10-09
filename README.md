# twitter-listener
twitter-listener is a small python script designed to notify you via Pushbullet (possibly more ways in the future!) of when a word that you choose is mentioned in a tweet! 

## Installing
**PLEASE NOTE**: Configuration  is **required** before using. This will not work out of box!!

 1. Head to the [releases](https://github.com/Mahlarian/twitter-listener/releases) section and download the latest version.
 2. Ensure you have python 3+ installed on your system.
 3. For ease, it's recommended to have **pipenv** installed as well to make grabbing dependencies easier and ensure a working install. You can download it easily with `pip install pipenv`
 4. With pipenv installed, run the command `pipenv install --ignore-pipfile`. This will install any dependencies on your system.
 5. Run `pipenv shell`, then `python3 main.py`

## Configuring
This script comes with several settings to adjust the behavior of the listener. 

 - `key:str`: This comes from your developer account in Twitter's API
 - `secret:str`: This comes from your developer account in Twitter's API
 - `bearer:str`: This comes from your developer account in Twitter's API
 - `access/token:str`: Found in the client section, this comes from your developer account in Twitter's API
 - `access/secret:str`: Found in the client section, this comes from your developer account in Twitter's API
 - `finder/search_frequency:int`: How often the finder will collect recent tweets and search them, measured in minutes. Set this to a value that matches the activity of the user to avoid unnecessary calls.
 - `finder/user_handle:str`: The `@username` part of the user's account. Do not include the `@` sign.
 - `finder/ignore_replies:bool`: This will ignore any replies from the user's account, including to themself. This is good for corporate accounts who provide support through their Twitter.
 - `finder/search_count:int`: How many tweets should the finder search? This can pull up to 3.2k of the user's most recent tweets. **Be aware that higher values could result in high resource costs/too many requests**
 - `finder/keyword:str`: What will cause the listener to notify you. This should be in all lowercase letters. If you want a specific word, try adding a space at the end. Not adding a space will cause the listener to search for those letters instead (eg: "the" will trigger if it finds the words "the", "their", "there", etc. in a tweet)
 - `finder/ignore_past_tweets:bool`: Should the listener ignore tweets in the past that contained your key word?
 - `finder/initial_scan_count:int`: The listener makes a scan of tweets at the start of running. How many tweets should it store in the history? 
 - `finder/memory:int`: The max amount of tweets the listener can store. Tweets that get stored into history after it's full will delete the oldest tweets.
 - `sender/push_bullet_token:str`: The token from your PushBullet account.
 - `sender/title:str`: The title of the notification when the listener identifies your keyword.
 - `sender/body:str`: The message content of the notification when the listener identifies your keyword.
 - `sender/msg_on_error:bool`: Should the listener send you a push notification if it encounters an error? **The listener will always log errors in the console regardless of this setting.**
 - `sender/msg_on_startup:bool`: Should the listener send you a push notification when it starts?
## Licensing

Copyright (c) Mahlarian, 2021. This project is protected and licensed under the [GNU General Public License v3.0](/LICENSE)
