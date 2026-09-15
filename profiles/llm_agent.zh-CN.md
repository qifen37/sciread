# LLM / Agent 专项 Profile

适用于使用 LLM、Planner、Tool、Retrieval 或 Multi-Agent 的论文。

重点核对：
- 固定 Agent 还是动态实例化；
- 是否有 Planner / Orchestrator；
- Expert Role；
- Shared / Isolated Memory；
- Static Broadcast / Dynamic Routing；
- Retrieval 来源与 Top-k；
- External Tool；
- Candidate Filtering；
- Iteration / Stop Rule；
- Feedback Loop；
- Backbone 依赖；
- 若论文报告，记录 Latency / Token / API Cost。

关键边界：
- RL Agent ≠ LLM Agent；
- Candidate Filtering 会限制下游召回上限；
- Generated Rationale ≠ Faithful Explanation；
- Mechanism-conditioned 可能只是 Prompt 层隐式推理，不代表显式机制变量。
