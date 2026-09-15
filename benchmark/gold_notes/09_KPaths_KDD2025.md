# 快读笔记

##### 1、论文标题：K-Paths: Reasoning over Graph Paths for Drug Repurposing and Drug Interaction Prediction（K-Paths：基于知识图谱路径的药物重定位与药物相互作用推理）

##### 2、研究问题：生物医学知识图谱包含大量药物、疾病、靶点和关系，但如何从大规模KG中提取对一个具体查询真正有用的证据仍然困难。传统subgraph retrieval通常为GNN设计，返回的大型子图不适合直接输入LLM；而简单最短路径又容易高度重复，缺乏关系多样性。K-Paths关注的问题是：能否构建一种训练无关、模型无关的检索器，从KG中为每个药物对/药物-疾病查询提取少量、结构化、关系多样且生物学有意义的多跳路径，使同一批证据既可供LLM zero-shot reasoning，也可用于提升GNN效率和可解释性。

##### 3、方法：提出K-Paths。给定查询实体对，框架基于Yen’s K-shortest loopless paths算法进行改造，在路径长度之外加入diversity-aware选择，避免K条路径只是同一关系模式的轻微变体；提取出的路径经过结构化/文本化后可以直接输入LLM，作为外部知识进行zero-shot预测和reasoning；同样的路径集合还可作为压缩后的KG子图供EmerGNN等GNN训练，在显著缩小KG规模的同时保留与查询最相关的结构信息。

##### 4、创新：

- **提出training-free、model-agnostic的Biomedical KG Retrieval框架。** K-Paths的核心创新不是再训练一个query-specific GNN retriever，而是从大型KG中直接抽取少量structured、biologically meaningful multi-hop paths，并让同一种retrieval结果能够同时被LLM与GNN消费，解决传统biomedical subgraph retrieval主要面向GNN、难以兼容LLM的问题。

- **对Yen’s K-shortest loopless paths进行diversity-aware改造。** 框架不仅追求路径短，还优先保留relation pattern更具多样性的路径，以减少K条结果被同一类型关系链重复占据。我的理解是，这一设计把“查询相关性”与“证据互补性”同时编码进retrieval，而不是简单列出多个最短路径。

- **把path作为统一的可解释reasoning interface，支持zero-shot LLM与inductive GNN。** 路径可被序列化为自然语言/结构化context直接提供给LLM，也可组成紧凑task-specific subgraph输入EmerGNN等模型；因此K-Paths同时提升zero-shot reasoning、unseen-entity inductive reasoning和监督GNN训练效率。论文还报告EmerGNN可在KG规模降低约90%的情况下保持较强性能，这体现了检索框架的效率贡献。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看KDD原论文整体流程图。）

##### 6、所用数据集：Drug-Drug Interaction + Drug Repurposing

- DrugBank：用于DDI type classification。
- DDInter：用于DDI severity classification。
- PharmacotherapyDB：用于drug repurposing。
- 论文同时覆盖LLM zero-shot reasoning、GNN supervised learning以及涉及训练阶段未见实体的inductive reasoning。

##### 7、缺点/局限：K-Paths最大的优势是简单、训练无关和可迁移，但它仍然依赖KG已有边：如果关键机制关系在KG中缺失，最优路径也无法恢复；短路径和relation diversity是启发式生物相关性代理，不保证每条路径都是真实因果机制。对于LLM，路径文本可以减少幻觉但不能消除语言模型自身推理错误；对于GNN，减少约90%的KG规模强调的是效率，不代表所有被删除关系都没有价值。

##### 8、个人评价（是否值得精读）：非常值得精读。K-Paths的思想非常干净：不重新训练一个复杂retriever，而是把“结构化、多样、短的证据链”做成统一接口，让LLM和GNN都能用。对于DDI+Agent尤其有启发，可以把K-Paths作为KG Tool，Agent只负责提出查询和选择机制方向，而不是把整张KG塞进Prompt。进一步可以结合pair-specific motif evidence，让路径检索受到分子结构条件约束。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- Biomedical KG：信息丰富但规模巨大 --> 全图GNN训练成本高 --> LLM更不可能直接处理整图。
- Subgraph retrieval：大多为GNN设计，输出节点/边集合 --> 对LLM而言缺乏自然的序列化reasoning unit。
- Path reasoning：多跳路径天然形成“实体-关系-实体”的解释链 --> 传统K shortest paths容易高度重复 --> 需要兼顾短路径与关系多样性。

##### 2、模型输入输出：

- 输入：查询实体对，例如Drug A–Drug B或Drug–Disease，以及一个大型生物医学KG。
- 输出：K条无环、多跳、关系多样的结构化路径；这些路径可以进一步被文本化输入LLM，或组成紧凑子图输入GNN。

##### 3、关键模块（每个模块的功能）：

- Query-specific Graph Search：以查询两端实体为起终点，只搜索与当前问题直接相连的候选路径。
- Yen’s K-Shortest Loopless Paths：以经典算法寻找多条无环候选路径，避免重复节点形成循环。
- Diversity-Aware Path Selection：在路径长度之外考虑relationship pattern差异，降低K条路径共享同一语义模板的冗余。
- Biological Relation Prioritization：优先保留具有生物医学意义的关系组合，使路径不仅短，还具有领域可解释性。
- Path Serialization：将KG path转化为LLM容易读取的结构化文本序列，形成外部context。
- LLM Zero-shot Reasoning：LLM在不进行任务特定训练的情况下，根据检索路径判断DDI severity或drug-disease relation。
- GNN Integration：将K-Paths作为原始KG的紧凑替代/子集，用于EmerGNN等模型，减少训练图规模并保持预测性能。
- Rationale Generation：路径本身可被展示为预测依据，但其解释属性来自“可追溯证据链”，并非因果验证。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：DrugBank、DDInter、PharmacotherapyDB。
- LLM实验：比较无外部KG路径、不同路径/上下文方案与K-Paths增强后的多种LLM，并重点评估zero-shot drug interaction与drug repurposing。
- GNN实验：将K-Paths得到的task-specific compact KG与EmerGNN等监督模型结合，比较完整KG与压缩KG下的预测性能和训练效率。
- 评估指标：主要使用Accuracy、F1和Kappa等分类指标，并报告KG压缩规模与训练效率。
- 泛化：论文特别关注unobserved interactions以及涉及training-time unseen entities的inductive inference。
- 实验设备：Gold Note不对论文未明确需要记录的硬件信息做推测。

##### 5、案例分析（做了什么样的案例）：

- 论文展示具体查询对应的多跳KG paths，让读者直接看到药物、靶点、疾病或机制实体如何形成推理链，并比较普通路径与diverse paths的信息覆盖。案例用来说明“为什么路径比整图/孤立文本更容易作为可解释context”，但这些路径应理解为数据库支持的证据链，而不是临床实验确认的机制。

##### 6、关键启发（哪些地方对自己有用）：K-Paths非常适合做Agent Tool，而不是直接作为最终DDI模型。一个更强的系统可以先由机制Planner提出“代谢/靶点/副作用”等查询方向，再用K-Paths从KG检索对应路径，同时由分子模型给出关键motif，最后在结构证据与KG路径之间做一致性检查。还可以做counterfactual path deletion：移除某条路径后观察预测变化，区分“被LLM引用的路径”和“真正影响决策的路径”。
