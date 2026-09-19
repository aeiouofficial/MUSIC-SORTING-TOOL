# AsmJit Readiness Plan — MUSIC-SORTING-TOOL

Status: PREPARED_ONLY
Branch: `prep/asmjit-readiness-2026-09-19`
Decision: DO NOT INTEGRATE.

The workload is music-file classification, naming, filesystem movement, metadata handling, and progress tracking. A custom native JIT does not address the current bottlenecks.

## Preferred optimization path
Profile filesystem traversal, metadata reads, classification rules, batching, concurrency, and incremental indexing.

## Revisit trigger
Only a future native runtime-specialized DSP/classification kernel with measured need.

No implementation, dependency addition, PR, or merge on this branch.
