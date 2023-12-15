import pandas as pd
from ntscraper import Nitter

def get_tweets(name, mode, no):
    scraper = Nitter()
    tweets = scraper.get_tweets(name, mode=mode, number=no)
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'], x['date'], x['stats']['likes'], x['stats']['comments']]
        final_tweets.append(data)
    df = pd.DataFrame(final_tweets, columns=['twitter_link', 'text', 'date', 'likes', 'comments'])
    return df

def main():
    # Example usage
    scraper = Nitter()

    # Get profile information for JeffBezos
    profile_info = scraper.get_profile_info("JeffBezos")
    print(profile_info)

    # Get profile information for BillGates
    bill_gates_info = scraper.get_profile_info('BillGates')
    print(bill_gates_info)

    # Get tweets for JeffBezos from our scraper
    tweets_df = get_tweets('JeffBezos', 'user', 6)
    print(tweets_df)

    

if __name__ == "__main__":
    main()
