# 快读笔记

##### 1、论文标题：Informative Subgraph Extraction with Deep Reinforcement Learning for Drug-Drug Interaction Prediction（用于DDI预测的深度强化学习信息子图提取）

##### 2、研究问题：基于知识图谱子图的DDI方法通常先从两个药物周围提取k-hop或固定规则子图，再交给GNN编码，但真实生物医学KG规模大、噪声多，固定k-hop会包含大量与当前药物对无关的节点；另一方面，现有子图选择通常只看KG拓扑，没有利用药物自身分子结构去判断“哪些知识关系对这一对药物最相关”。因此本文关注的核心问题是：如何把子图提取本身变成一个针对药物对动态优化的决策过程，并同时利用KG上下文和分子结构指导选择。

##### 3、方法：提出RISE-DDI，将informative subgraph extraction建模为Markov Decision Process，并使用Deep Reinforcement Learning Agent逐步选择/扩展药物对相关子图。RL agent的动作决定保留哪些候选节点/关系，状态反映当前子图和药物对信息；为了避免只根据拓扑做选择，作者设计Structure-Aware Reward Model，将KG局部结构特征与Drug Pair Molecular Features共同纳入奖励，鼓励Agent提取既与当前结构上下文相关、又与两个药物分子特征一致的context-specific subgraph。提取后的子图再用于下游DDI预测。

##### 4、创新：

- **将DDI知识子图提取显式建模为Markov Decision Process，并用Deep RL进行query-specific extraction。** 这是作者第一项核心贡献：不再依赖固定k-hop、PageRank或其他静态规则，而是让RL sampler针对每个drug pair在候选KG空间中顺序决策，动态选择最有信息量的context-specific subgraph。

- **设计learnable Structure-Aware Reward，把KG topology与drug-pair molecular features共同作为子图质量信号。** 作者针对现有方法“只看KG结构、忽略药物分子特异性”的缺口，让interaction predictor不仅承担最终DDI预测，还为sampler提供奖励，使Agent倾向选择既有拓扑意义、又与当前药物分子结构相关的证据子图。

- **在transductive与inductive场景验证RL extraction并给出可视化机制证据。** 作者第三项贡献包括三个benchmark上的系统实验、最高约20%的提升以及extracted subgraph visualization。这里真正值得强调的不是“用了RL”本身，而是把**证据检索策略作为可学习决策过程**；同时必须区分：论文里的Agent是reinforcement-learning agent，并非LLM/Multi-Agent。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看AAAI原论文模型图。）

##### 6、所用数据集：二分类（传导 + 归纳）

- DrugBank
- KEGG
- OGB-biokg
- 官方代码分别提供三个数据集的transductive与inductive训练配置。

##### 7、缺点/局限：RISE-DDI的创新主要在“怎么抽子图”，下游预测框架本身不是核心突破；强化学习带来更灵活的选择，但也增加训练复杂度和reward design依赖。Structure-Aware Reward仍是可学习代理目标，不能保证提取子图等价于真实药理机制；子图可视化说明模型找到了一组相关证据，但没有证明这些边是预测必要条件。值得注意的是，这里的“Agent”是强化学习Agent，不是LLM/Multi-Agent，不应混为一谈。

##### 8、个人评价（是否值得精读）：值得精读，尤其值得看子图抽取部分。它对“全图信息太多、固定子图太粗”这个问题抓得比较准确，并把分子结构用于KG检索条件，和普通k-hop方法相比有实质改进。对后续工作可以进一步把RL选择从node/subgraph层升级到relation/path/mechanism层，并加入可微或反事实验证，避免reward学到仅有利于分类但缺乏生物意义的捷径。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- Full-KG方法：全图或大邻域聚合信息丰富 --> 同时引入大量噪声和计算开销。
- Fixed Subgraph方法：k-hop、random walk、PageRank等能够缩小范围 --> 对所有query采用相似规则 --> 无法根据Drug A/Drug B结构差异动态选择证据。
- Molecular Structure：DDI与分子官能团/结构有关 --> 如果只根据KG topology抽图，会忽略当前pair的化学特异性 --> 因此把结构特征加入subgraph reward。

##### 2、模型输入输出：

- 输入：查询药物对、全局生物医学KG、两个药物的分子结构特征。
- 输出：针对该drug pair的informative subgraph，以及基于该子图得到的DDI二分类预测。

##### 3、关键模块（每个模块的功能）：

- Candidate Context Construction：围绕查询药物对建立候选KG区域，限定RL搜索空间。
- MDP Formulation：把当前已选择子图定义为state，把加入/保留候选节点或关系定义为action，形成逐步子图构建过程。
- RL Subgraph Extraction Agent：学习在不同state下采取动作，以最大化累计reward，实现每个药物对不同的动态抽图策略。
- KG Topology Encoder：表示候选节点/边在KG中的局部拓扑和关系上下文，为state和reward提供图信息。
- Molecular Feature Encoder：提取两个药物的分子结构特征，使子图选择与当前Drug Pair化学特征相关。
- Structure-Aware Reward Model：综合subgraph topology与molecular features评估选择质量，为RL Agent提供学习信号。
- Subgraph Encoder / Predictor：对最终选择的子图进行GNN式编码，结合drug pair表示完成DDI分类。
- Inductive Inference：在新药场景下仍根据分子结构和KG局部上下文动态提取证据，避免完全依赖训练中见过的drug node embedding。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：DrugBank、KEGG、OGB-biokg。
- 设置：分别评估transductive与inductive DDI prediction；最困难场景涉及测试drug在训练中完全未见。
- Baselines：覆盖GNN-based、KG-based与subgraph-based DDI方法，并额外比较k-hop、DeepWalk、PageRank等不同subgraph extraction策略。
- 评估指标：AUC、AUPR、ACC、F1等二分类指标。
- 结果：原文报告在不同benchmark/setting上优于SOTA，最具挑战的unseen-drug场景提升最高约20%。
- 组件验证：分别分析RL-based sampler、structure-aware reward、子图大小/搜索参数以及inductive场景中的贡献。
- 实验设备：官方仓库主要在Linux + NVIDIA A100 40GB环境测试。

##### 5、案例分析（做了什么样的案例）：

- 论文比较不同子图提取策略得到的节点/关系，展示RL Agent能够过滤固定k-hop中大量无关分支，并保留与Drug Pair结构或已知生物关系更一致的路径。案例主要验证subgraph selection的针对性和可读性；其“机制”性质来自知识图谱语义支持，而不是因果干预。

##### 6、关键启发（哪些地方对自己有用）：RISE-DDI最直接的启发是“KG不是越多越好，关键是query-conditioned evidence retrieval”。如果做下一步，可以不让RL只选择节点，而是让Agent选择mechanism prototype → relation type → path，再用分子motif作为条件；同时用预测变化作为counterfactual reward的一部分，要求被选择证据在功能上对结果有贡献。这样可以把informative subgraph进一步推进到faithful subgraph。
