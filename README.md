# SciRead

> Structured, evidence-grounded, contribution-faithful scientific paper reading for research workflows.

Current release: **v0.6.0**

[中文说明](README.zh-CN.md)

## What SciRead does

SciRead is a model-agnostic reading specification for turning a paper into a reusable research note rather than a generic summary.

It emphasizes:
- correct task formulation;
- author-grounded contribution extraction;
- full method reconstruction;
- experiment fidelity;
- strong-claim calibration;
- explicit missing-information handling;
- research-useful critique and inspiration.

`SKILL.md` is the canonical English specification.  
`SKILL.zh-CN.md` is the official Chinese translation.

## Quick start

For a DDI paper:

> Read `SKILL.md` and `profiles/ddi.md`, then analyze this paper using SciRead.

For DDI + LLM/Agent:

> Read `SKILL.md`, `profiles/ddi.md`, and `profiles/llm_agent.md`, then analyze this paper using SciRead.

## Repository

```text
SciRead/
├── SKILL.md
├── SKILL.zh-CN.md
├── AGENTS.md
├── README.md
├── README.zh-CN.md
├── profiles/
├── templates/
├── rubrics/
├── benchmark/
│   ├── gold_notes/
│   └── metadata.json
├── registry/
├── scripts/
└── docs/
```

## Benchmark

The bundled DDI reference set contains 12 audited Full Gold Notes.

They are source-verified and model-curated, not independently human-annotated.

The benchmark is a depth/reference set, not a clean held-out evaluation.

## Validation

```bash
python scripts/validate.py
```

The validator checks:
- required project files;
- 12 Gold Notes;
- Gold Note structure;
- consolidated benchmark metadata;
- contribution mappings;
- evidence ledgers;
- version locks;
- negative-fact registries.

## Dataset Registry

`registry/ddi_datasets.yaml` is **validation-only**.

It must never be used to silently fill a paper's missing task, version, label count, or split.

## License

MIT.
