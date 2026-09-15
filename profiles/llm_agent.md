# LLM / Agent Profile

Use with `SKILL.md` when a paper uses LLMs, planners, tools, retrieval, or multi-agent systems.

Check:
- fixed vs dynamic agents;
- planner/orchestrator;
- expert roles;
- shared vs isolated memory;
- static broadcast vs dynamic routing;
- retrieval source and top-k policy;
- external tools;
- candidate filtering;
- number of rounds / stopping rule;
- feedback loop;
- backbone model dependence;
- latency/token/API cost when reported.

Important distinctions:
- RL agent ≠ LLM agent;
- candidate filtering can cap downstream recall;
- generated rationale ≠ faithful explanation;
- mechanism-conditioned language may still be implicit prompt reasoning rather than an explicit mechanism variable.

If later rounds do not actually change agents/tools/context, do not overstate “dynamic” iteration.
