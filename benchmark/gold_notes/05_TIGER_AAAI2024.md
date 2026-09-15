# 快读笔记

##### 1、论文标题：Dual-Channel Learning Framework for Drug-Drug Interaction Prediction via Relation-Aware Heterogeneous Graph Transformer（基于关系感知异构图Transformer的双通道DDI预测框架）

##### 2、研究问题：现有基于网络的DDI方法大多依赖局部邻域聚合，随着GNN层数增加才能获得远距离信息，但容易出现信息过平滑或难以捕获长程依赖；同时，DDI预测既需要药物自身分子图的内部结构，也需要生物医学知识图谱中的外部语义关系，已有方法通常只强调其中一侧或者采用较粗粒度融合。TIGER因此关注两个问题：如何用Transformer直接建模异构KG中的长距离、高阶结构，以及如何将分子图内部结构与KG全局上下文通过双通道方式联合用于DDI预测。

##### 3、方法：提出TIGER。模型构建两个并行通道：Molecular Graph Channel从单药分子图学习图级结构表示；Biomedical Knowledge Graph Channel将药物、靶点、疾病等实体形成异构图，并通过Relation-Aware Heterogeneous Graph Transformer建模远距离节点依赖和多种关系语义。关系感知自注意力在计算节点间注意力时显式引入relation information，使不同语义边对信息传递产生不同影响；最后将分子图级表示与KG节点级表示融合，对药物对进行DDI预测。

##### 4、创新：

- **提出graph-level + node-level的双通道异构图DDI框架。** 作者第一项贡献是用dual-channel heterogeneous graph approach统一处理两类互补信息：一条通道从drug molecular graph学习graph-level结构表示，另一条从biomedical knowledge graph中学习以药物为中心的node-level上下文，再融合得到最终drug representation。其创新不是简单“双模态拼接”，而是明确对应药物内部结构与外部生物医学关系两个层级。

- **设计Relation-Aware Self-Attention处理异构KG中的多重语义关系。** 普通Transformer难以区分同一node pair间不同关系的语义，TIGER将relation information直接纳入self-attention，在sampled drug-centered subgraph中学习long dependencies和high-order structures，同时保留multiple semantic relations。

- **通过sampled subgraph上的Transformer实现全局/高阶依赖而避免直接处理整张大型BKG。** 原文强调TIGER的node-level representation不是把整个KG一次性送入Transformer，而是围绕每个drug node采样固定规模子图后进行relation-aware graph transformer编码。作者第三项贡献是用三个真实数据集和case study验证预测性能与机制理解能力；从方法角度看，这一设计使“异构KG的长程关系建模”在计算上更可行。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看原论文整体框架图。）

##### 6、所用数据集：DDI预测（三个真实世界数据集）

- DrugBank：1052种drugs、10404条verified DDIs。
- KEGG：786种drugs、13787条DDIs。
- OGB-biokg：808种drugs、111520条DDIs。
- 三个数据集均结合各自的biomedical heterogeneous graph和drug molecular graphs进行DDI link prediction；实验采用等量负样本并进行5-fold cross-validation。

##### 7、缺点/局限：TIGER的核心是“两个通道分别编码，再融合”，仍然主要得到每个药物的通用表示，Drug A与Drug B之间具体哪些局部子结构、KG关系因当前pair而重要没有被显式条件化。Transformer全局注意力虽然能看到远距离信息，但在大规模KG中也会引入计算和噪声问题；Relation-Aware Attention说明模型关注不同关系，但注意力权重本身不能直接视为机制因果证据。案例中的机制解释更适合作为plausibility evidence，而不是faithful reasoning证明。

##### 8、个人评价（是否值得精读）：值得精读。TIGER是“分子图 + 生物医学KG”双通道路线中很典型、也很容易成为后续baseline的一篇。它的价值主要在架构设计和relation-aware Transformer，而不是某个特别复杂的训练目标。对于后续研究，最值得改的是将静态双通道融合升级为pair-aware cross-modal interaction，让结构证据和KG证据针对当前药物对动态对齐，而不是先独立压缩再融合。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- KG/GNN路线：已有模型使用生物医学网络聚合邻域 --> GCN/GAT通常依赖局部message passing --> 对长距离、高阶依赖捕获有限，层数加深又可能过平滑。
- 分子结构路线：molecular graph可以表达原子和化学键 --> 但单纯结构不能覆盖靶点、疾病、通路等系统生物学信息 --> 因此需要结构图与异构KG双通道。
- Transformer路线：全局注意力擅长长依赖 --> 直接用于异构KG时还需要处理relation semantics --> 引出Relation-Aware Heterogeneous Graph Transformer。

##### 2、模型输入输出：

- 输入：两个药物的molecular graph；包含药物及相关生物医学实体和多种relation的heterogeneous KG。
- 输出：给定药物对的DDI预测结果。

##### 3、关键模块（每个模块的功能）：

- Molecular Graph Channel：在原子-键分子图上进行图表示学习，提取药物内部拓扑和化学结构特征，最终得到graph-level embedding。
- Heterogeneous KG Construction：将药物、靶点、疾病等不同实体以及多种生物医学关系组织为异构图，为外部语义建模提供基础。
- Relation-Aware Self-Attention：在query/key/value交互中加入关系类型相关表示，使不同relation对注意力得分和消息传递有不同影响。
- Heterogeneous Graph Transformer：通过Transformer式全局交互捕获远距离节点依赖和高阶图结构，相比固定hop GNN降低对深层堆叠的依赖。
- Dual-Channel Representation：分别保留分子图的graph-level表示与KG的node-level表示，避免在早期就把两类信息混在一起。
- Fusion & Prediction：将两通道药物表示融合，对药物对进行最终DDI打分/分类。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：DrugBank、KEGG、OGB-biokg。
- 任务：将DDI prediction表述为基于BKG与molecular graphs的link prediction，并为正样本构造等量negative drug pairs。
- Baselines：覆盖传统network embedding、GNN/KG方法以及multi-level DDI方法，原文重点与KGNN、MIRACLE、MDNN等代表方法比较。
- 评估指标：ACC、F1、AUC、AUPR。
- 主要实现：PyTorch 1.10.2；50 epochs；Adam，learning rate 0.001；embedding维度64；relation-aware graph transformer层数L=2；采用drug-centered sampled subgraphs而非整图Transformer。
- 实验设备：官方实现主要在Linux + NVIDIA A100 40GB环境测试；作者同时说明模型可在16GB RAM的Mac上训练。

##### 5、案例分析（做了什么样的案例）：

- 论文通过case study展示模型如何同时利用分子结构和生物医学网络关系来理解一个药物对：一方面观察molecular graph中的结构特征，另一方面追踪KG中与药物、靶点或其他实体相关的高阶连接，从而给出比单一路径模型更完整的解释。该案例用于说明Relation-Aware Transformer能够捕获具有语义差异的远距离关系，并体现双通道信息互补；但论文没有通过删除关键关系或结构片段的方式验证这些证据对最终预测是否具有必要性，因此更适合视为解释潜力展示。

##### 6、关键启发（哪些地方对自己有用）：TIGER可以作为后续“静态双通道”设计的典型参照。进一步工作可以不再独立得到Drug A和Drug B的固定表示，而是在motif/substructure级做cross-attention，同时让KG relation作为动态条件；这样能够回答“Drug A在面对Drug B时关注哪部分结构、哪条KG机制证据”。此外，Transformer在KG上的全局能力与子图检索并不是互斥的：可以先用pair-specific retrieval降噪，再用relation-aware Transformer做高阶推理。
