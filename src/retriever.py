import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TicketRetriever:
    def __init__(self, data_path="data/sample_for_labeling.csv"):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", data_path)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.X = None
        self.df = None
        self._load_and_index()
        
    def _load_and_index(self):
        if not os.path.exists(self.data_path):
            print(f"[WARN] Retriever could not find {self.data_path}")
            return
            
        self.df = pd.read_csv(self.data_path)
        # Drop rows with missing text
        self.df = self.df.dropna(subset=['text_customer', 'text_brand'])
        self.X = self.vectorizer.fit_transform(self.df['text_customer'].astype(str))
        
    def search(self, query, k=3):
        if self.X is None or self.df is None or self.df.empty:
            return []
            
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.X).flatten()
        top_indices = similarities.argsort()[-k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05: # Slight threshold
                results.append({
                    "customer_tweet": self.df.iloc[idx]['text_customer'],
                    "brand_reply": self.df.iloc[idx]['text_brand'],
                    "score": similarities[idx]
                })
        return results

if __name__ == "__main__":
    retriever = TicketRetriever()
    res = retriever.search("My battery is dying so fast since the update!")
    for r in res:
        print(f"Score {r['score']:.2f}")
        print(f"Cust: {r['customer_tweet']}")
        print(f"Brand: {r['brand_reply']}\n")
