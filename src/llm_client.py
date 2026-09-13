import os
import json
from retriever import TicketRetriever

# Lazy load retriever to avoid slow start if not querying
_retriever_instance = None

def get_retriever():
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = TicketRetriever()
    return _retriever_instance

def classify_and_draft(tweet_text):
    """
    1. Retrieve context
    2. Classify intent
    3. Draft reply grounded on context
    4. Escalation decision
    """
    # Use Gemini API
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("\n[WARN] GEMINI_API_KEY missing. Using Mock LLM Fallback...", end="", flush=True)
        import random
        return {
            "intent": random.choice(['account_issue', 'hardware_issue', 'software_issue', 'order_and_billing', 'other']),
            "draft_reply": "This is a mock draft reply since the AI key is missing. Please DM us your device info.",
            "escalate": False,
            "escalation_reason": "N/A"
        }
        
    genai.configure(api_key=api_key)
    # Use gemini-2.5-pro or gemini-2.5-flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 1. Retrieval
    retriever = get_retriever()
    similar_cases = retriever.search(tweet_text, k=3)
    
    context_str = ""
    if similar_cases:
        context_str = "Here is how similar queries were resolved by human agents in the past:\n"
        for i, case in enumerate(similar_cases):
            context_str += f"Example {i+1}:\nCustomer: {case['customer_tweet']}\nAgent Reply: {case['brand_reply']}\n\n"
    
    prompt = f"""
    You are an AI support agent for AppleSupport on Twitter.
    A customer just tweeted: "{tweet_text}"
    
    {context_str}
    
    Perform three tasks:
    1. Intent: Classify the customer's intent into one of: 'account_issue', 'hardware_issue', 'software_issue', 'order_and_billing', 'other'
    2. Draft: Write a short, empathetic Twitter reply (under 280 chars) offering initial troubleshooting or asking to DM for details. Use the human agent examples provided (if any) as a stylistic and procedural guide. Do not use hashtags if possible.
    3. Escalate: Should this be escalated to a human immediately (true/false) and why? (Escalate if aggressive, legally sensitive, or needs secure account info).
    
    Output strictly in this JSON format without markdown code blocks:
    {{
        "intent": "...",
        "draft_reply": "...",
        "escalate": true,
        "escalation_reason": "..."
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        text = response.text
        # Fallback manual parsing if mime_type formatting introduces extra text
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        out = json.loads(text[json_start:json_end])
        out['rag_history'] = similar_cases
        return out
    except Exception as e:
        return {
            "intent": "other",
            "draft_reply": "Sorry, an error occurred processing this request.",
            "escalate": True,
            "escalation_reason": f"Parsing failed: {e}"
        }
