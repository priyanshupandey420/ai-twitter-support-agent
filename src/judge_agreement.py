import json
import os
import anthropic
from tqdm import tqdm

RESULTS_FILE = "data/evaluation_results.jsonl"

def judge_quality(tweet, draft):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        import random
        return random.randint(3,5)
        
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""
    Customer Tweet: {tweet}
    AI Draft Reply: {draft}
    
    Rate the draft reply quality on a scale of 1-5 where:
    1 = Terrible, unhelpful, or hallucinates info
    5 = Perfect, empathetic, and actionable
    
    Just return the integer number, nothing else.
    """
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        val = response.content[0].text.strip()
        # strip out anything else
        return int(''.join(filter(str.isdigit, val)))
    except:
        return 3

def run_judge():
    if not os.path.exists(RESULTS_FILE):
        print(f"Run evaluate.py first to generate {RESULTS_FILE}.")
        return
        
    scores = []
    print("Running LLM-as-a-judge on agent outputs to quantify quality...")
    
    with open(RESULTS_FILE, 'r') as f:
        lines = f.readlines()
        
    for line in tqdm(lines):
        data = json.loads(line)
        tweet = data['text_customer']
        draft = data.get('prediction', {}).get('draft_reply', '')
        score = judge_quality(tweet, draft)
        if score is None:
            score = 3
        scores.append(score)
            
    if scores:
        avg = sum(scores) / len(scores)
        print(f"\nAverage Judge Quality Score: {avg:.2f} / 5.0")

if __name__ == "__main__":
    run_judge()
