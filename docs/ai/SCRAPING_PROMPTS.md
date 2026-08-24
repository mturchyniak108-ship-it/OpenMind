# AI Scraping Prompt Templates

## Structured Extraction

```text
Extract only fields supported by the supplied document.
Return JSON only.
Missing values must be null.
Do not guess.
Preserve exact names and dates.
Include evidence for important claims.
```

## Classification

```text
Classify the supplied document.
Return JSON containing category, relevance, reason, and confidence.
Use only evidence contained in the document.
```

## Research Summary

```text
Summarize the supplied documents.
Separate direct facts, source claims, interpretations, uncertainty, and conflicting evidence.
Do not convert source claims into established facts.
```
