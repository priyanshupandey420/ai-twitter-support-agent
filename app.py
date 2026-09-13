import streamlit as st
import sys
import os

# Add src to path so we can import our pipeline
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from llm_client import classify_and_draft

st.set_page_config(page_title="AI Support Agent", page_icon="🤖", layout="wide")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Enter your Gemini API key below to enable the RAG pipeline.")
    api_key = st.text_input("Google Gemini API Key:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        
    st.divider()
    st.subheader("🧠 How it Works")
    st.markdown("""
    1. **Retrieval**: When a tweet arrives, we query a vector database (`scikit-learn` TF-IDF) of historically resolved AppleSupport conversations.
    2. **Grounding**: We pass the top 3 similar cases to **Gemini 2.5**.
    3. **Action**: The AI classifies the intent, evaluates if a human is urgently needed (Escalation), and drafts a highly empathetic response mirroring the historical human agents.
    """)
    st.caption("Built for Hiver SDE evaluation.")

# --- MAIN CHAT INTERFACE ---
st.title("🤖 AI Twitter Support Agent")
st.markdown("A highly contextual Support Agent powered by Gemini 2.5 and Historical Ticket RAG.")

# Initialize chat session state if missing
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous chats (just for visual effect)
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Customer Input
if tweet_input := st.chat_input("Paste a frustrated customer tweet here..."):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("🚨 Please enter a Gemini API Key in the sidebar first!")
    else:
        # 1. Add User Tweet to Chat
        st.session_state.history.append({"role": "user", "content": tweet_input})
        with st.chat_message("user"):
            st.markdown(tweet_input)

        # 2. Add AI Agent processing block
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing intent & retrieving historical tickets..."):
                result = classify_and_draft(tweet_input)
            
            # --- Results Presentation ---
            st.markdown(f"**{result.get('draft_reply', 'Error drafting reply.')}**")
            
            # Analytics Dashboard
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                intent_val = result.get("intent", "Unknown").replace("_", " ").title()
                st.metric("Categorized Intent", intent_val)
                
            with col2:
                escalate = result.get("escalate", False)
                if escalate:
                    st.error("🚨 ESCALATION REQUIRED")
                    st.caption(f"**Reason:** {result.get('escalation_reason', 'N/A')}")
                else:
                    st.success("✅ Standard Handling (No Escalation)")
            
            # RAG History Expander
            rag_history = result.get("rag_history", [])
            if rag_history:
                with st.expander("🔍 View AI Thought Process (RAG Context)"):
                    st.markdown("The AI used these past resolved tickets to ground its response:")
                    for i, case in enumerate(rag_history):
                        st.info(f"**Case {i+1} (Match Score: {case['score']:.2f})**")
                        st.markdown(f"**Customer:** {case['customer_tweet']}")
                        st.markdown(f"**Agent:** {case['brand_reply']}")
                        
        # Save AI response to history so it stays on screen
        st.session_state.history.append({"role": "assistant", "content": result.get('draft_reply')})
