import pandas as pd
import os
import tweepy
from dotenv import load_dotenv
import os
import botometer


load_dotenv()

rapidapi_key = os.environ["RAPID_KEY"]

consumer_key = os.environ["API_KEY"]
consumer_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

# auth = tweepy.OAuth1UserHandler(
#   consumer_key,
#   consumer_secret,
#   access_token,
#   access_token_secret
# )
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret,
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


def get_info(tweet_id):
    info_tweet = api.get_status(tweet_id, tweet_mode="extended")
    try:
        user_info = bom.check_account(info_tweet.user.id_str)
    except:
        user_info=None
    if user_info:
        fake_follower_score=user_info['raw_scores']['english']['fake_follower']
        spammer_score=user_info['raw_scores']['english']['spammer']
        overall_score=user_info['raw_scores']['english']['overall']
        self_dec_score=user_info['raw_scores']['english']['self_declared']
        return {'ID': info_tweet.id,
        'Tweet': info_tweet.full_text,
        'Date': info_tweet.created_at,
        'Location': info_tweet.user.location,
        'user_follower': info_tweet.user.followers_count,
        'user_friend': info_tweet.user.friends_count,
        'user_favourite': info_tweet.user.favourites_count,
        'user_description': info_tweet.user.description,
        'user_verfied': info_tweet.user.verified,
        'lang': info_tweet.lang,
        'retweet': info_tweet.retweet_count,
        'favourite':info_tweet.favorite_count,
        'fake_follower':fake_follower_score,
         'self_declared':self_dec_score,
        'overall':overall_score,
         'spammer_score': spammer_score}
    else:
        return {'ID': info_tweet.id,
                'Tweet': info_tweet.full_text,
                'Date': info_tweet.created_at,
                'Location': info_tweet.user.location,
                'user_follower': info_tweet.user.followers_count,
                'user_friend': info_tweet.user.friends_count,
                'user_favourite': info_tweet.user.favourites_count,
                'user_description': info_tweet.user.description,
                'user_verfied': info_tweet.user.verified,
                'lang': info_tweet.lang,
                'retweet': info_tweet.retweet_count,
                'favourite': info_tweet.favorite_count,
                'fake_follower':0,
                'self_declared':0,
                'overall':0,
                'spammer_score': 0}

cmu_misinfo=pd.read_csv("/home/ricky/PycharmProjects/SM_fakenews/SM_data/CMU_MisCov19_dataset.csv",sep=',')

true_tweets=[]
false_tweets=[]
count=0
for ii,rows in cmu_misinfo.iterrows():
    print(ii)
    try:
        if 'false' in rows['annotation1'] or 'fake' in rows['annotation1']:
            false_tweets.append(get_info(rows['status_id']))

        elif 'true' in rows['annotation1']:
            true_tweets.append(get_info(rows['status_id']))
    except:
        count+=1

false_tweets_df=pd.DataFrame(false_tweets)
false_tweets_df['label']=0

true_tweets_df=pd.DataFrame(true_tweets)
true_tweets_df['label']=1

final_df=pd.concat((true_tweets_df,false_tweets_df))
final_df.to_csv('./SM_data/CMU_tweets.csv',sep='\t',index=False)