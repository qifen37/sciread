# DDI Profile

Use with `SKILL.md` for drug–drug interaction papers.

## Task gate
Identify the exact formulation:
- binary DDI existence;
- multi-class event;
- multi-label side effect;
- ranking/recommendation;
- zero-shot event;
- explanation generation.

## DrugBank
Never infer a protocol from the word `DrugBank` alone. Verify:
- version if reported;
- label space;
- binary vs multi-class use;
- event count;
- split protocol;
- known/new drug definitions;
- directionality.

## TWOSIDES
Verify whether the paper uses:
- binary per-side-effect classification;
- multi-label prediction;
- ranking/recommendation.

## Generalization
Distinguish:
- transductive;
- unseen pair;
- unseen drug;
- known-known / known-new / new-new;
- zero-shot unseen event;
- temporal generalization.

## Molecular representation
Classify what is actually used:
- fingerprint;
- SMILES;
- molecular graph;
- motif / BRICS;
- pharmacophore;
- learned substructure;
- 3D geometry;
- pretrained molecular model.

## KG usage
Distinguish:
- KG embedding;
- neighbor message passing;
- heterogeneous GNN;
- subgraph extraction;
- path reasoning;
- retrieval;
- textualization;
- Agent context/tool.

## Interpretability
Identify the evidence type:
- attention;
- atom/substructure/pharmacophore importance;
- KG path/subgraph;
- node/path deletion;
- counterfactual intervention;
- natural-language rationale.

Do not equate plausibility with faithfulness.

## Mechanism claims
If the paper says mechanism-aware/conditioned, determine whether mechanism is:
- explicit;
- supervised;
- prototype/pathway/relation based;
- latent;
- retrieved;
- only implicitly inferred by an LLM.

## Registry rule
`registry/ddi_datasets.yaml` is validation-only. It may flag inconsistency; it may not supply a missing paper fact.
