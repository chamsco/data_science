import tweepy
import yaml 

# Step 1 - Authenticate


def load_creds(file):
    with open(file, 'r', encoding="utf-8") as file:
        creds = yaml.safe_load(file)
        return creds
        

# Step 2 - Connect / Use the API endpoints

def create_api():
    creds= load_creds('auth/auth.cred.yml')
    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])

    api = tweepy.API(auth,wait_on_rate_limit=True)
    
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e
    
    return api