import pandas as pd
import os
import json

SAMPLES_FILE = "data/sample_for_labeling.csv"
LABELS_FILE = "data/golden_labels.jsonl"
INTENTS = ["account_issue", "hardware_issue", "software_issue", "order_and_billing", "other"]

def run_labeler():
    if not os.path.exists(SAMPLES_FILE):
        print(f"Error: {SAMPLES_FILE} not found. Run sample_for_labeling.py first.")
        return
        
    df = pd.read_csv(SAMPLES_FILE)
    
    # Load existing to resume
    labeled_ids = set()
    if os.path.exists(LABELS_FILE):
        with open(LABELS_FILE, 'r') as f:
            for line in f:
                data = json.loads(line)
                labeled_ids.add(data['tweet_id_customer'])
    
    print(f"Already labeled {len(labeled_ids)} / {len(df)}. Starting CLI...")
    
    with open(LABELS_FILE, 'a') as f:
        for idx, row in df.iterrows():
            if row['tweet_id_customer'] in labeled_ids:
                continue
                
            print("\n" + "="*50)
            print(f"TWEET {idx+1}/{len(df)}")
            print(f"CUSTOMER: {row['text_customer']}")
            print(f"BRAND (for context): {row['text_brand']}")
            print("="*50)
            print("Categories:")
            for i, intent in enumerate(INTENTS):
                print(f"  {i+1}. {intent}")
            print("  s. skip")
            print("  q. quit")
            
            while True:
                choice = input("Select category (1-5, s, q): ").strip().lower()
                
                if choice == 'q':
                    print("Quitting.")
                    return
                elif choice == 's':
                    print("Skipping...")
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(INTENTS):
                    label = INTENTS[int(choice)-1]
                    record = {
                        "tweet_id_customer": row['tweet_id_customer'],
                        "text_customer": row['text_customer'],
                        "tweet_id_brand": row['tweet_id_brand'],
                        "text_brand": row['text_brand'],
                        "label": label
                    }
                    f.write(json.dumps(record) + "\n")
                    print(f"-> Saved as '{label}'")
                    break
                else:
                    print("Invalid choice. Try again.")

if __name__ == "__main__":
    run_labeler()
