# Human Review Protocol

SciRead v0.5 is **source-verified and model-curated**. This protocol defines the minimum process required before calling the benchmark independently human-validated.

## Reviewers

Recommended: 3 independent reviewers.
- at least one DDI/bioinformatics domain researcher;
- at least one ML/GNN researcher;
- a third reviewer from either domain.

Reviewers should not see each other's labels during the first pass.

## Units to score

For every Gold Note score:
1. Research Problem
2. Method
3. Innovation / Contribution Fidelity
4. Task Formulation
5. Dataset / Split / Metric Fidelity
6. Key Modules
7. Case Study Fidelity
8. Limitations / Claim Calibration
9. Research Insight Separation
10. Overall Factuality

Labels:
- `2 = Correct`
- `1 = Partially correct / materially incomplete`
- `0 = Incorrect / unsupported`

Also record `cannot_judge` separately; do not force a score when source expertise/evidence is insufficient.

## Contribution review

For every author-stated contribution C1...Cn verify:
- represented in the Gold Note;
- not strengthened beyond the paper;
- reader interpretation is clearly bounded;
- no extra Innovation bullet is presented as author contribution without mapping.

## Adjudication

After blind scoring:
1. compute pairwise agreement and Fleiss' kappa on non-missing labels;
2. discuss disagreements;
3. produce an adjudicated note/version;
4. preserve both pre-adjudication labels and final adjudication.

## Suggested release threshold

Do not label the benchmark `Human Gold` until:
- each note has >=2 independent expert reviews;
- mean Correct/Partial score is reported;
- inter-annotator agreement is reported;
- all `Incorrect` contribution/task/dataset claims are adjudicated.

No target kappa is mandated because prevalence and three-level labels affect kappa, but low agreement must be disclosed rather than hidden.
