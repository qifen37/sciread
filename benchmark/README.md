# DDI Reference Benchmark

SciRead v0.6 ships with 12 audited DDI Full Gold Notes covering different methodological families.

The notes are **source-verified and model-curated reference notes**. They are not independently human-annotated ground truth.

## Contents

- `gold_notes/` — 12 complete Chinese research notes.
- `metadata.json` — consolidated provenance, contribution maps, version locks, negative facts, coverage requirements, and audit metadata.

## Intended use

Gold Notes are used as:
- output-depth references;
- regression references;
- examples of contribution-faithful DDI reading.

They are **not** to be copied into a new paper analysis.

## Method families

The benchmark covers:
- substructure learning;
- KG neural networks;
- multimodal fusion;
- multi-relational contrastive learning;
- heterogeneous graph Transformer;
- zero-shot unseen-event prediction;
- motif/topology refinement;
- natural-language explanations;
- KG path retrieval;
- RL subgraph extraction;
- pharmacophore modeling;
- multi-agent dynamic knowledge flow.

## Evidence policy

For important claims, metadata may record:
- exact page;
- exact section;
- source only.

Lower precision is preferable to invented precision.

## Benchmark status

These 12 papers were used during SciRead development, so they are DEV/reference materials, not clean held-out evaluation.

Independent human review is still required before calling the benchmark Human Gold.
