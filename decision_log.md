# Decision Log

1. **Brand Selection**: Chosen `AppleSupport`. Why? It's one of the highest-volume brands in the dataset, and Apple support tickets cleanly divide into clear taxonomy (Hardware, Software, Account, Billing).
2. **Framework Missing**: Decided to build the entire "starter repo" architecture from scratch including evaluation harness, labeller CLI, and intent mappings because none of the starter files were injected in the directory.
3. **LLM Decision Pipeline**: Combined classification, drafting, and escalation into a single LLM API call using structured JSON format rather than multi-stage chaining to save latency and token costs.
4. **Escalation Rules**: Defaulted to human escalation whenever there is a parsing error to degrade gracefully.
