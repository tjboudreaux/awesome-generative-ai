import tweepy
import re
import os

# Use environment variables for credentials and Twitter username
API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET_TOKEN = os.environ['ACCESS_SECRET_TOKEN']
TWITTER_USERNAME = os.environ['TWITTER_USERNAME']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

api = tweepy.API(auth)


def is_ai_related(text):
    ai_keywords = ['artificial intelligence', 'AI', 'machine learning',
                   'deep learning', 'neural network', 'NLP', 'natural language processing']
    for keyword in ai_keywords:
        if keyword.lower() in text.lower():
            return True
    return False


def get_links(text):
    return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


def read_existing_links(readme_path):
    ai_related_links = []
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                link = get_links(line)
                if link:
                    ai_related_links.append((line.strip(), link[0]))
    return ai_related_links


def main(username):
    ai_related_likes = read_existing_links('README.md')
    tweets = api.favorites(screen_name=username, count=100)

    for tweet in tweets:
        if is_ai_related(tweet.text) and tweet.favorite_count > 100:
            links = get_links(tweet.text)
            if links:
                title_and_link = (tweet.text, links[0])
                if title_and_link not in ai_related_likes:
                    ai_related_likes.append(title_and_link)

    header = "# AI-related Twitter Likes\n"
    with open('README.md', 'w') as f:
        f.write(header)
        for title, link in ai_related_likes:
            f.write(f'- [{title}]({link})\n')


if __name__ == '__main__':
    main(TWITTER_USERNAME)
