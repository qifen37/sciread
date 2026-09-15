# SciRead Quality Rubric

This single rubric consolidates factuality, contribution fidelity, critical reading, and note quality.

## 1. Factuality
A strong note:
- reports only source-supported facts;
- explicitly leaves missing information missing;
- keeps dataset/task/split details paper-specific;
- avoids imported facts from related papers.

## 2. Research problem
The note should reconstruct:
- existing paradigm;
- concrete limitation;
- why it matters;
- the paper's reframing/solution.

## 3. Innovation fidelity
The Innovation section should:
- map to author-stated contributions;
- explain what is technically new;
- explain which prior limitation is addressed;
- distinguish method novelty from empirical results;
- preserve attribution for “first” claims.

## 4. Method completeness
For major modules, cover:
- purpose;
- input;
- operation;
- output;
- connection to the pipeline.

## 5. Experimental fidelity
Correctly map:
- dataset;
- task formulation;
- split;
- baselines;
- metrics;
- backbone;
- implementation/hardware only when reported.

## 6. Case-study fidelity
If a case study exists, preserve:
- starting query/state;
- intermediate reasoning/evidence;
- final prediction/interpretation;
- what the case actually demonstrates.

If none exists, say so.

## 7. Strong-claim calibration
### Causal
Look for intervention, deletion, counterfactual, treatment/control semantics, or causal identification. Do not call attention causal.

### Mechanism
Determine whether mechanism is explicit, supervised, prototype/pathway/relation-based, latent, retrieved, or implicit.

### Faithful
Prefer evidence of functional dependence: deletion, sufficiency/necessity, counterfactual intervention, prediction sensitivity.

### Biological grounding
Distinguish:
1. plausible biological narrative;
2. database-supported relation;
3. literature-supported mechanism;
4. experimental validation.

## 8. Research-transfer value
Key Inspiration should produce concrete research operations, not generic praise.

Examples:
- make an implicit mechanism variable explicit;
- replace static fusion with pair-conditioned routing;
- use GNN/KG tools inside an Agent;
- add counterfactual evidence deletion;
- combine cold-start with long-tail evaluation.

## 9. Information density
A note should be detailed enough for research use but not repetitive.

Structural compliance alone is not sufficient.

## 10. Suggested 50-point evaluation
- Research problem precision: 0–5
- Method pipeline completeness: 0–5
- Contribution fidelity: 0–5
- Module-level technical detail: 0–5
- Experimental fidelity: 0–5
- Case-study fidelity: 0–5
- Critical analysis: 0–5
- Research-transfer value: 0–5
- Information density: 0–5
- Factuality: 0–5

Interpretation:
- 45–50: Gold-quality
- 40–44: strong
- 34–39: usable but incomplete
- 25–33: over-compressed / important omissions
- <25: poor
