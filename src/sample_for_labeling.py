import pandas as pd
import os

PROCESSED_FILE = "data/processed_conversations.csv"
SAMPLES_FILE = "data/sample_for_labeling.csv"
SAMPLE_SIZE = 200

def run_sampling():
    if not os.path.exists(PROCESSED_FILE):
        print(f"Error: {PROCESSED_FILE} not found. Run ingest.py first.")
        return

    df = pd.read_csv(PROCESSED_FILE)
    print(f"Loaded {len(df)} total conversations.")
    
    if len(df) < SAMPLE_SIZE:
        print(f"Warning: Only found {len(df)} rows, taking all.")
        sample_df = df
    else:
        sample_df = df.sample(n=SAMPLE_SIZE, random_state=42)
    
    sample_df.to_csv(SAMPLES_FILE, index=False)
    print(f"Saved {len(sample_df)} samples to {SAMPLES_FILE} for manual labeling.")

if __name__ == "__main__":
    run_sampling()
