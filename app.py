from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from ntscraper import Nitter

app = Flask(__name__)

def get_tweets(name, mode, no):
    try:
        scraper = Nitter()
        tweets = scraper.get_tweets(name, mode=mode, number=no)
        final_tweets = []

        for x in tweets['tweets']:
            date_without_time = pd.to_datetime(x['date'], format='%b %d, %Y · %I:%M %p UTC').strftime('%b %d, %Y')
            data = [x['link'], x['text'], date_without_time, x['stats']['likes'], x['stats']['comments']]
            final_tweets.append(data)

        df = pd.DataFrame(final_tweets, columns=['twitter_link', 'text', 'date', 'likes', 'comments'])

        # Additional code for user_data retrieval
        user_data = None
        if mode == 'user':
            profile_info = scraper.get_profile_info(name)
            user_data = {
                'username': profile_info['username'],
                'name': profile_info['name'],
                'bio': profile_info['bio'],
                'image': profile_info['image'],
                'followers': profile_info['stats']['followers'],
                'following': profile_info['stats']['following']
            }

        return df, user_data, None  # No error message

    except Exception as e:
        error_message = f"An Unknown error occurred: {e}. Please try again. Or try another, Eg. User (UserID to be entered in the search term) - imVkohli, BillGates etc"
        print(error_message)
        return pd.DataFrame(), None, error_message




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    mode = request.form['mode']
    no = int(request.form['no'])
    result_tuple = get_tweets(name, mode, no)
    tweets_df, user_data, error_message = result_tuple
    return render_template('result.html', name=name, mode=mode, no=no, tweets_df=tweets_df, user_data=user_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
