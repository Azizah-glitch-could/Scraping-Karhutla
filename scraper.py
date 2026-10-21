import tweepy
import pandas as pd
from config import BEARER_TOKEN

def scrape_karhutla_tweets(target_count=1000):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    query = "karhutla OR (kebakaran hutan) OR (kebakaran lahan) -is:retweet lang:id"
    
    tweets_list = []
    
    print("Mulai mengambil data Twitter...")
    
    try:
        paginator = tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            max_results=100,  # Max 100 per request
            tweet_fields=['created_at', 'lang', 'public_metrics', 'author_id']
        )
        
        for response in paginator:
            if response.data:
                for tweet in response.data:
                    metrics = tweet.public_metrics
                    tweets_list.append({
                        'tweet_id': tweet.id,
                        'created_at': tweet.created_at,
                        'text': tweet.text,
                        'retweet_count': metrics['retweet_count'],
                        'reply_count': metrics['reply_count'],
                        'like_count': metrics['like_count'],
                        'quote_count': metrics['quote_count']
                    })
                    
                    if len(tweets_list) >= target_count:
                        break
            
            print(f"Data terkumpul: {len(tweets_list)} baris")
            if len(tweets_list) >= target_count:
                break
                
    except Exception as e:
        print(f"Terjadi kendala saat mengambil data: {e}")

    # Konversi ke Pandas DataFrame
    df = pd.DataFrame(tweets_list)
    
    # Simpan ke file CSV
    output_filename = "data_karhutla.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\nSelesai! Data {len(df)} baris berhasil disimpan ke '{output_filename}'")

if __name__ == "__main__":
    scrape_karhutla_tweets(target_count=1000)