# Inference Pipeline

```text
Input
  -> Prompt
  -> Tokenizer
  -> Model Runtime
  -> Hidden State
  -> Generation
  -> Output
```

Representation instrumentation must remain optional.

Always retain a baseline inference path for comparison.

Compare baseline, instrumented, and candidate optimized paths using the same workload whenever possible.
