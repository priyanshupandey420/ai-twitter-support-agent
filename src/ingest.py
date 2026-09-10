import pandas as pd
import os

DATA_FILE = "data/twcs.csv"
OUTPUT_FILE = "data/processed_conversations.csv"
TARGET_BRAND = "AppleSupport"

def run_ingest():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        print("Please download from Kaggle: kaggle datasets download thoughtvector/customer-support-on-twitter -p data --unzip")
        return

    print("Loading dataset (this may take a moment due to 3M rows)...")
    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    print(f"Filtering for brand: {TARGET_BRAND}...")
    brand_tweets = df[df['author_id'] == TARGET_BRAND]
    print(f"Found {len(brand_tweets)} replies by {TARGET_BRAND}")
    
    inbound_tweets = df[df['tweet_id'].isin(brand_tweets['in_response_to_tweet_id'].dropna())]
    
    # Merge to get conversations: [inbound_tweet, brand_reply]
    conversations = pd.merge(
        inbound_tweets, 
        brand_tweets, 
        left_on='tweet_id', 
        right_on='in_response_to_tweet_id', 
        suffixes=('_customer', '_brand')
    )
    
    # Filter for valid dialogues
    conversations = conversations[['text_customer', 'text_brand', 'tweet_id_customer', 'tweet_id_brand']]
    
    print(f"Found {len(conversations)} resolved pairs for {TARGET_BRAND}.")
    
    conversations.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved processed conversations to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_ingest()
