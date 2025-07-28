import tweepy
import pandas as pd
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterSentimentCollector:
    def __init__(self):
        """Initialize Twitter API client"""
        # Twitter API credentials (you'll need to get these from Twitter Developer Portal)
        self.api_key = os.getenv('TWITTER_API_KEY', 'your_api_key_here')
        self.api_secret = os.getenv('TWITTER_API_SECRET', 'your_api_secret_here')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN', 'your_access_token_here')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', 'your_access_token_secret_here')
        
        # Initialize API client
        try:
            auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            self.client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN', 'your_bearer_token_here'),
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            self.connected = True
        except Exception as e:
            print(f"Twitter API connection failed: {e}")
            print("Using mock data instead...")
            self.connected = False
    
    def search_tweets(self, query, count=100, lang='en'):
        """Search for tweets with given query"""
        if not self.connected:
            return self._get_mock_tweets(query, count)
        
        try:
            tweets = []
            for tweet in tweepy.Cursor(self.api.search_tweets, 
                                     q=query, 
                                     lang=lang, 
                                     tweet_mode='extended').items(count):
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'user': tweet.user.screen_name,
                    'created_at': tweet.created_at,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'followers_count': tweet.user.followers_count
                })
            return tweets
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return self._get_mock_tweets(query, count)
    
    def get_user_tweets(self, username, count=100):
        """Get tweets from a specific user"""
        if not self.connected:
            return self._get_mock_user_tweets(username, count)
        
        try:
            tweets = []
            for tweet in tweepy.Cursor(self.api.user_timeline, 
                                     screen_name=username, 
                                     tweet_mode='extended').items(count):
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'user': tweet.user.screen_name,
                    'created_at': tweet.created_at,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count
                })
            return tweets
        except Exception as e:
            print(f"Error getting user tweets: {e}")
            return self._get_mock_user_tweets(username, count)
    
    def get_trending_topics(self, woeid=1):  # 1 = worldwide
        """Get trending topics"""
        if not self.connected:
            return self._get_mock_trending_topics()
        
        try:
            trends = self.api.get_place_trends(woeid)
            return [trend['name'] for trend in trends[0]['trends'][:10]]
        except Exception as e:
            print(f"Error getting trending topics: {e}")
            return self._get_mock_trending_topics()
    
    def _get_mock_tweets(self, query, count):
        """Generate mock tweets for testing"""
        mock_tweets = [
            {
                'id': 123456789,
                'text': f"Just tried the new {query} and it's absolutely amazing! Love it!",
                'user': 'user1',
                'created_at': datetime.now(),
                'retweet_count': 15,
                'favorite_count': 45,
                'followers_count': 1200
            },
            {
                'id': 123456790,
                'text': f"The {query} is terrible. Worst experience ever!",
                'user': 'user2',
                'created_at': datetime.now() - timedelta(hours=1),
                'retweet_count': 8,
                'favorite_count': 12,
                'followers_count': 500
            },
            {
                'id': 123456791,
                'text': f"Using {query} for the first time. It's okay, nothing special.",
                'user': 'user3',
                'created_at': datetime.now() - timedelta(hours=2),
                'retweet_count': 2,
                'favorite_count': 5,
                'followers_count': 800
            },
            {
                'id': 123456792,
                'text': f"Can't believe how good {query} is! Best thing I've ever used!",
                'user': 'user4',
                'created_at': datetime.now() - timedelta(hours=3),
                'retweet_count': 25,
                'favorite_count': 67,
                'followers_count': 2000
            },
            {
                'id': 123456793,
                'text': f"Disappointed with {query}. Expected much better quality.",
                'user': 'user5',
                'created_at': datetime.now() - timedelta(hours=4),
                'retweet_count': 3,
                'favorite_count': 8,
                'followers_count': 300
            }
        ]
        return mock_tweets[:count]
    
    def _get_mock_user_tweets(self, username, count):
        """Generate mock user tweets"""
        return self._get_mock_tweets(f"@{username}", count)
    
    def _get_mock_trending_topics(self):
        """Generate mock trending topics"""
        return [
            "#MachineLearning",
            "#AI",
            "#DataScience", 
            "#Python",
            "#TechNews",
            "#Innovation",
            "#Startup",
            "#Programming",
            "#ArtificialIntelligence",
            "#BigData"
        ]
    
    def analyze_twitter_sentiment(self, query, count=100, analyzer=None):
        """Analyze sentiment of tweets for a given query"""
        tweets = self.search_tweets(query, count)
        
        if not tweets:
            return {
                'query': query,
                'total_tweets': 0,
                'sentiment_distribution': {},
                'tweets': [],
                'error': 'No tweets found'
            }
        
        # Analyze sentiment for each tweet
        analyzed_tweets = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for tweet in tweets:
            if analyzer:
                sentiment_result = analyzer.predict_sentiment(tweet['text'])
                tweet['sentiment'] = sentiment_result['sentiment']
                tweet['confidence'] = sentiment_result['confidence']
                sentiment_counts[sentiment_result['sentiment']] += 1
            else:
                # Simple keyword-based sentiment if no analyzer provided
                text_lower = tweet['text'].lower()
                positive_words = ['love', 'great', 'amazing', 'excellent', 'best', 'good', 'wonderful']
                negative_words = ['hate', 'terrible', 'awful', 'worst', 'bad', 'disappointed', 'terrible']
                
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    tweet['sentiment'] = 'positive'
                    sentiment_counts['positive'] += 1
                elif negative_count > positive_count:
                    tweet['sentiment'] = 'negative'
                    sentiment_counts['negative'] += 1
                else:
                    tweet['sentiment'] = 'neutral'
                    sentiment_counts['neutral'] += 1
                
                tweet['confidence'] = 0.7  # Mock confidence
            
            analyzed_tweets.append(tweet)
        
        # Calculate percentages
        total = len(analyzed_tweets)
        sentiment_distribution = {
            'positive': (sentiment_counts['positive'] / total) * 100,
            'negative': (sentiment_counts['negative'] / total) * 100,
            'neutral': (sentiment_counts['neutral'] / total) * 100
        }
        
        return {
            'query': query,
            'total_tweets': total,
            'sentiment_distribution': sentiment_distribution,
            'sentiment_counts': sentiment_counts,
            'tweets': analyzed_tweets,
            'timestamp': datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    collector = TwitterSentimentCollector()
    
    # Test trending topics
    trends = collector.get_trending_topics()
    print("Trending topics:", trends)
    
    # Test tweet search
    tweets = collector.search_tweets("machine learning", count=5)
    print(f"Found {len(tweets)} tweets")
    
    for tweet in tweets:
        print(f"@{tweet['user']}: {tweet['text'][:100]}...") 