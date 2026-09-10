# AI Support Agent Evaluation Report

## 1. Problem Framing
What "good" means for AppleSupport:
- **Fast, accurate resolution**: Customers tweeting Apple usually have software integration bugs, hardware failure states, or account locks.
- **Tone**: Empathetic and highly professional.
- **Escalation Policy**: Specific issues (like potential hacks, legally sensitive statements, or payment disputes) require human escalation. General queries should be handled or routed to a generic DM.

## 2. Results vs Baselines
*(Fallback Mock Execution Results due to missing API Key)*
| Model / Pipeline | Intent Accuracy (%) | Reply Quality (1-5) | 
| ----- | ------------ | ------------- |
| Trivial Baseline (Majority Class) | ~20% | N/A |
| Final AI Support Agent (Mocked Fallback) | 22.0% | 3.98 / 5.0 |

## 3. Failure Analysis
Because we are running on the Mock AI fallback, failures present uniformly across the 5 categories since the AI model randomly picks an intent.
1. The model completely misses context (it's hardcoded to random).
2. It offers the same fallback draft "Please DM us" regardless of the severity.
3. It fails to catch escalation terms.

## 4. What is Misleading About the Headline Number?
- Subjective human labeling means the ground truth has intrinsic noise.
- LLM-as-a-judge calibrates higher/more predictably on LLM-generated output, inflating quality metrics.

## 5. What I'd Do with One More Week
- Add dense vector retrieval (RAG) to embed historical brand-customer resolved pairs to directly inform the prompt's drafting style, rather than just standard zero-shot drafting.
