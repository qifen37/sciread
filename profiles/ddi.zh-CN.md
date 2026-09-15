# DDI 专项 Profile

与 `SKILL.zh-CN.md` 配合使用。

## Task Gate
必须先确认：
- 二分类 DDI；
- 多分类事件；
- 多标签副作用；
- Ranking / Recommendation；
- Zero-shot Event；
- Explanation Generation。

## DrugBank
不能只看到 `DrugBank` 就自动套固定协议。必须核对：
- 版本；
- Label Space；
- 二分类还是多分类；
- 事件类别数；
- 数据划分；
- Known/New Drug 定义；
- 是否有方向性。

## TWOSIDES
必须确认是：
- 每个副作用单独二分类；
- 多标签预测；
- Ranking / Recommendation。

## 泛化设置
区分：
- Transductive；
- Unseen Pair；
- Unseen Drug；
- Known-Known / Known-New / New-New；
- Unseen Event；
- Temporal Generalization。

## 分子表示
明确属于：
- Fingerprint；
- SMILES；
- Molecular Graph；
- Motif / BRICS；
- Pharmacophore；
- Learned Substructure；
- 3D；
- Pretrained Molecular Model。

## KG 使用方式
区分：
- KG Embedding；
- 邻域消息传播；
- Heterogeneous GNN；
- Subgraph Extraction；
- Path Reasoning；
- Retrieval；
- Textualization；
- Agent Context / Tool。

## 可解释性
明确证据类型：
- Attention；
- 原子/子结构/药效团重要性；
- KG Path / Subgraph；
- Node/Path Deletion；
- Counterfactual Intervention；
- Natural-Language Rationale。

合理解释不等于 Faithful Explanation。

## 机制 Claim
若论文写 mechanism-aware / conditioned，必须说明机制是：
- 显式变量；
- 有监督；
- Prototype / Pathway / Relation；
- Latent；
- Retrieved；
- 还是仅由 LLM Prompt 隐式推断。

## Registry
`registry/ddi_datasets.yaml` 只用于核查，不允许补论文没有报告的值。
