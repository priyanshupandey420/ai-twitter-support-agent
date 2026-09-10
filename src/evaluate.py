import json
import os
from tqdm import tqdm
import sys

# Add current dir so it can find llm_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from llm_client import classify_and_draft

LABELS_FILE = "data/golden_labels.jsonl"
RESULTS_FILE = "data/evaluation_results.jsonl"

def run_evaluation():
    if not os.path.exists(LABELS_FILE):
        print(f"Error: {LABELS_FILE} not found. Map the dataset and run the labeller first.")
        return
        
    correct = 0
    total = 0
    
    print("Starting AI agent evaluation on manually labeled golden set...")
    with open(LABELS_FILE, 'r') as f_in, open(RESULTS_FILE, 'w') as f_out:
        lines = f_in.readlines()
        for line in tqdm(lines):
            data = json.loads(line)
            actual_label = data['label']
            tweet = data['text_customer']
            
            try:
                result = classify_and_draft(tweet)
                predicted = result['intent']
                
                if predicted == actual_label:
                    correct += 1
                total += 1
                
                data['prediction'] = result
                f_out.write(json.dumps(data) + "\n")
            except Exception as e:
                print(f"\nFailed processing tweet (API missing/error): {e}")
                break
                
    if total > 0:
        accuracy = correct / total
        print(f"\nAccuracy vs human baselines: {(accuracy*100):.2f}% ({correct}/{total})")
    else:
        print("\nNo evaluation performed.")

if __name__ == "__main__":
    run_evaluation()
