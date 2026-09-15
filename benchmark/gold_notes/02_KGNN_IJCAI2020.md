# 快读笔记

##### 1、论文标题：KGNN: Knowledge Graph Neural Network for Drug-Drug Interaction Prediction（KGNN：用于药物-药物相互作用预测的知识图谱神经网络）

##### 2、研究问题：早期DDI方法通常通过整合药物相似度、分子描述符或不同数据源进行预测，而使用知识图谱的方法也大多停留在为每个实体直接学习静态embedding，未充分利用药物与靶点、基因、疾病等实体之间的局部邻域结构。对于DDI而言，一个药物的潜在相互作用往往与其多跳生物医学关系相关，因此只学习单个节点向量会丢失高阶拓扑和关系语义。本文的核心问题是：如何端到端地从生物医学知识图谱中聚合与药物相关的多跳邻居，同时让不同关系和中心实体本身共同影响邻域信息，以提升DDI二分类预测。

##### 3、方法：提出KGNN。模型首先根据DrugBank或KEGG-drug构建生物医学知识图谱，并为每个药物采样固定大小的邻居；随后采用多层邻域聚合，将邻居实体表示与关系表示共同组合，同时利用当前中心实体的表示对邻居信息进行加权，使感受野随层数扩展到多跳结构；最后得到两个药物的知识增强表示，并通过打分函数预测药物对是否发生相互作用。整个模型以端到端方式学习，不再把KG embedding与分类器割裂开来。

##### 4、创新：

- **提出面向DDI的Knowledge Graph Neural Network端到端框架。** 据作者表述，KGNN是其所知首个将“knowledge graph neural network”作为完整DDI预测框架的工作：不再只对KG实体学习静态latent embedding，而是直接探索药物在知识图谱中的topological structures，并通过扩展receptive field捕获drug pair之间的高阶关联。

- **将KG的拓扑邻域、关系语义与当前药物条件联合纳入聚合。** 作者将这一点概括为KGNN的三个technical highlights：利用每个实体的topological information；从local receptive field聚合邻域以提取high-order structures与semantic relations；再用与上述信息兼容的GNN完成潜在DDI预测。我的理解是，其真正突破点在于把“KG作为静态特征来源”推进为“KG作为可消息传播的上下文结构”。

- **以更少的药物专用输入实现知识增强DDI预测。** 原文强调KGNN不需要额外的chemical structure或专门设计的drug representation，仅依赖DDI matrix与构建的KG完成端到端学习；实验贡献则用于验证这种高阶KG邻域建模相较经典embedding/网络方法的有效性。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看原论文Figure 1。）

##### 6、所用数据集：二分类（随机划分，传导设置为主）

- DrugBank v5.1.4：2578种药物、612388条已知相互作用；对应知识图谱约212万实体、72类关系、785万三元组。
- KEGG-drug：1925种药物、56983条相互作用；对应知识图谱约13万实体、167类关系、36万三元组。
- 正样本按照8:1:1随机划分训练/验证/测试，并从非相互作用药物对中按相同数量采样负样本。

##### 7、缺点/局限：KGNN的重要贡献在当时是把KG邻域信息真正用于DDI，但邻域是固定大小采样并逐层聚合，容易引入大量与特定药物对无关的节点；其“相关性”主要由单药中心表示决定，还没有显式建模Drug A与Drug B之间的pair-specific条件。模型主要是二分类存在性预测，因此对于具体DDI事件类型的机制差异刻画有限。此外，随机划分会让训练和测试共享大量药物，不能直接说明对完全新药的泛化能力。

##### 8、个人评价（是否值得精读）：值得精读，尤其适合作为“DDI + Biomedical KG”方向的基础工作。它现在看起来并不复杂，但清楚展示了从静态KG embedding向可学习邻域聚合的转变。对于后续SumGNN、EmerGNN、TIGER、RISE-DDI等KG方法，KGNN是很好的技术脉络起点。真正需要改进的是从“以单药为中心的通用邻域”走向“以药物对和候选机制为条件的动态证据选择”。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- 多源DDI方法：整合指纹、结构、靶点、疾病等侧信息 --> 常见做法是先独立做embedding再拼接 --> 数据源之间的高阶拓扑关系没有被端到端利用。
- KG方法：TransE等知识图谱表示可以编码实体和关系 --> 但通常输出固定节点向量 --> 对一个药物真正相关的多跳邻域、不同关系类型和长距离关联利用不足 --> 因此作者引入GNN式局部感受野和多层聚合。

##### 2、模型输入输出：

- 输入：DDI二分类矩阵/药物对，以及由Bio2RDF等方式构建的生物医学知识图谱；KG中包含药物及其相关实体和关系。
- 输出：两个药物之间是否存在DDI的预测值。

##### 3、关键模块（每个模块的功能）：

- KG构建与泄漏控制：从DrugBank和KEGG相关资源构建KG，同时移除显式DDI关系，避免模型在KG中直接读取测试目标。
- Neighbor Sampling：对每个实体随机采样固定数量邻居，使多跳聚合计算可控；论文设置邻居数16。
- Relation-aware Neighbor Representation：将邻居实体和对应关系表示组合，保留“连接到什么实体”以及“以什么关系连接”两类信息。
- Neighborhood Aggregation：使用当前中心实体的表示对邻居信息进行加权，再将聚合结果与中心实体自身表示结合；通过堆叠两层扩展到更高阶的KG邻域。
- Drug Pair Scoring：得到两个药物的知识增强表示后，通过打分函数计算相互作用概率，并与二分类标签联合训练。
- End-to-End Optimization：KG实体/关系表示、邻域聚合和DDI分类目标共同更新，使知识表示直接服务于DDI预测，而不是预训练后固定。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：
  - DrugBank v5.1.4；
  - KEGG-drug。
- Baselines：
  - Laplacian、GraRep、DeepWalk、struc2vec、LINE、SDNE、GAE；
  - DeepDDI；
  - KG-DDI。
- 评估指标：ACC、AUPR、AUC-ROC、F1，结果报告多次运行平均值。
- 主要超参数：batch size 4096、embedding维度32、GNN深度2、邻居数16、学习率1e-2；训练50 epochs。
- 实验设备：论文公开正文没有以可复用方式突出具体GPU型号。

##### 5、案例分析（做了什么样的案例）：

- KGNN论文并没有像后续可解释DDI工作那样给出具体药物对的机制案例。其“Case Study”主要是参数/结构敏感性分析，例如比较neighborhood sampling size、receptive field depth以及embedding dimension等设置，观察KGNN从多少跳邻居中获益。因而这里应把它理解为**模型行为分析**，而不是药理机制解释；Gold Note不额外编造具体drug–target–pathway案例。

##### 6、关键启发（哪些地方对自己有用）：KGNN最值得借鉴的是“知识图谱不应该只是另一个embedding输入”，而应该让查询药物主动从KG中聚合上下文。后续可以进一步把聚合条件从单药表示升级为药物对表示：让Drug A选择的KG邻居依赖Drug B，反之亦然；再进一步可以把关系类型聚类为机制原型，加入pair-conditioned routing和反事实删除，从而把“高阶邻域有效”提升到“哪些知识证据对当前DDI事件真正必要”。
