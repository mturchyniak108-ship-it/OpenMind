# Development Guide

Keep changes small, testable, reviewable, and reversible.

Before committing:

```bash
python -m compileall -q .
git diff --check
git status
```

Run the relevant project tests before committing.
