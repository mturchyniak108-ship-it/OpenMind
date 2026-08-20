# OpenMind TODO

## Knowledge Waveform Research

- [ ] Define canonical start_node/end_node path object
- [ ] Define relationship tags and direction encoding
- [ ] Define deterministic WAV/PCM encoding
- [ ] Define truth-confidence signal representation
- [ ] Define evidence-strength representation
- [ ] Define contradiction representation
- [ ] Define provenance representation
- [ ] Define path-cost representation
- [ ] Define multi-channel waveform format
- [ ] Build waveform encoder
- [ ] Build waveform decoder
- [ ] Verify lossless round-trip
- [ ] Generate demonstration knowledge waveforms
- [ ] Compare WAV storage with graph/vector storage
- [ ] Benchmark waveform generation latency
- [ ] Benchmark waveform lookup latency
- [ ] Benchmark path similarity
- [ ] Benchmark path ranking
- [ ] Test cycle reduction
- [ ] Test contradiction detection
- [ ] Test cross-language consistency
- [ ] Compare against traditional vector retrieval
- [ ] Compare against traditional LLM/RAG retrieval
- [ ] Determine whether waveform encoding provides measurable benefit

## Architecture Rule

Truth Graph = canonical knowledge.
WAV = derived experimental signal.
Provenance = required evidence trail.
No waveform representation may silently replace canonical structured truth.
