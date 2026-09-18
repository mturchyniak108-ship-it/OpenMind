# AI Scraping and Data Extraction

AI should assist with extraction planning, schema design, classification, deduplication, normalization, entity resolution, summarization, and quality review.

AI should not be treated as the original source of scraped facts.

## Collection Rules

1. Check applicable terms and policies.
2. Prefer official APIs and permitted feeds.
3. Respect robots.txt where applicable.
4. Respect rate limits.
5. Do not bypass authentication, paywalls, CAPTCHAs, or technical access controls.
6. Minimize collection of personal information.
7. Preserve source URLs and retrieval timestamps.

## Pipeline

```text
Source -> Fetcher -> Raw Document -> Parser -> Normalized Record -> AI Extraction -> Validation -> Provenance
```

The fetcher should retrieve source material deterministically. AI should operate on the retrieved content.

## AI Extraction Rules

- Return structured data.
- Do not invent missing values.
- Use null for unavailable fields.
- Preserve source wording for important claims.
- Record uncertainty.
- Preserve the original document.

## Provenance

Record source URL, retrieval timestamp, document hash, extraction model, prompt version, schema version, output, and validation state.

AI extraction is a transformation of source material, not proof that the source claims are true.
