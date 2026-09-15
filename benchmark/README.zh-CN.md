# DDI 参考 Benchmark

SciRead v0.6 保留 12 篇经过多轮审查的 DDI Full Gold Note，覆盖不同技术路线。

这些笔记属于：

> **source-verified, model-curated reference notes**

还不是独立人工标注的 Human Gold。

## 内容

- `gold_notes/`：12 篇完整中文科研阅读笔记。
- `metadata.json`：合并后的来源、Contribution Mapping、Version Lock、Negative Facts、Coverage 和 Audit 信息。

## 用途

Gold Note 只用于：
- 参考输出深度；
- 做回归检查；
- 参考 DDI 论文应该覆盖哪些内容。

不能直接复制旧论文的结论到新论文。

## 覆盖技术路线

包括：
- 子结构学习；
- KG GNN；
- 多模态融合；
- 多关系对比学习；
- Heterogeneous Graph Transformer；
- Zero-shot Event；
- Motif + Topology Refinement；
- 自然语言解释；
- KG Path Retrieval；
- RL Subgraph Extraction；
- Pharmacophore；
- Multi-Agent Dynamic Knowledge Flow。

## 证据原则

重要 Claim 可以记录：
- 精确页码；
- 精确 Section；
- 仅来源。

宁可定位精度低，也不允许猜页码。

## 当前状态

这 12 篇论文参与过 SciRead 的开发，因此属于 DEV / Reference，不是干净的 Held-out Test。

在没有独立人工审查前，不称为 Human Gold。
