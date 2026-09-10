import os
import json
import anthropic

def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n[WARN] ANTHROPIC_API_KEY missing. Using Mock LLM Fallback...", end="")
        return None
    return anthropic.Anthropic(api_key=api_key)

def classify_and_draft(tweet_text):
    """
    1. Classify intent
    2. Draft reply
    3. Escalation decision
    """
    client = get_client()
    
    if not client:
        # Fallback Mock logic
        import random
        return {
            "intent": random.choice(['account_issue', 'hardware_issue', 'software_issue', 'order_and_billing', 'other']),
            "draft_reply": "This is a mock draft reply since the AI key is missing. Please DM us your device info.",
            "escalate": False,
            "escalation_reason": "N/A"
        }
        
    prompt = f"""
    You are an AI support agent for AppleSupport on Twitter.
    A customer just tweeted: "{tweet_text}"
    
    Perform three tasks:
    1. Intent: Classify the customer's intent into one of: 'account_issue', 'hardware_issue', 'software_issue', 'order_and_billing', 'other'
    2. Draft: Write a short, empathetic Twitter reply (under 280 chars) offering initial troubleshooting or asking to DM for details. Do not use hashtags if possible.
    3. Escalate: Should this be escalated to a human immediately (true/false) and why? (Escalate if aggressive, legally sensitive, or needs secure account info).
    
    Output strictly in this JSON format:
    {{
        "intent": "...",
        "draft_reply": "...",
        "escalate": true,
        "escalation_reason": "..."
    }}
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        text = response.content[0].text
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        return json.loads(text[json_start:json_end])
    except Exception as e:
        return {
            "intent": "other",
            "draft_reply": "Sorry, an error occurred processing this request.",
            "escalate": True,
            "escalation_reason": f"Parsing failed: {e}"
        }
