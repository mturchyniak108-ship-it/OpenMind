# AI Scraping Data Schema

Recommended normalized record:

```json
{
  "source_url": "",
  "retrieved_at": "",
  "content_hash": "",
  "title": null,
  "published_at": null,
  "source_type": "",
  "content": "",
  "extraction_model": "",
  "prompt_version": "",
  "schema_version": "",
  "extracted": {},
  "validation": {"status": "unvalidated", "notes": ""}
}
```

Keep raw source content separate from AI-generated fields.
