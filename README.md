# AI Support Agent

This repository contains an AI customer support agent for Twitter built as part of the Hiver SDE Intern take-home assignment.

## Setup Instructions (Under 15 Mins)

1. **Install Python 3.10+ and setup environment**

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Credentials**
   Ensure you have the following environment variables set:
   - `ANTHROPIC_API_KEY`: Your Anthropic API Key for the LLM.
   - `KAGGLE_USERNAME` & `KAGGLE_KEY`: Your Kaggle API credentials (or place `kaggle.json` in the standard location).

4. **Download Dataset**
   ```bash
   kaggle datasets download -d thoughtvector/customer-support-on-twitter -p data --unzip
   ```

5. **Run Ingestion and Data Prep**
   ```bash
   python src/ingest.py
   ```

6. **Sample and Label Data (Golden Set)**
   ```bash
   python src/sample_for_labeling.py
   python src/label_cli.py
   ```

7. **Evaluate Agent**
   ```bash
   python src/evaluate.py
   python src/judge_agreement.py
   ```
