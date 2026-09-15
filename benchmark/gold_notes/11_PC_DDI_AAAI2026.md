# 快读笔记

##### 1、论文标题：Closer to Biological Mechanism: Drug-Drug Interaction Prediction from the Perspective of Pharmacophore（更接近生物学机制：从药效团视角预测DDI）

##### 2、研究问题：现有基于分子结构相似度的方法通常默认“结构相似的药物更可能产生相似交互”，但整分子结构中可能包含大量与当前药理作用无关的片段，直接在原子/子结构层学习容易捕捉不完整或不活跃的结构，既限制新药泛化，也让解释结果难以对应真实功能。作者认为药效团比普通motif更接近药物发挥生物活性的功能单元，因此尝试从pharmacophore视角建模DDI，并进一步识别对预测具有关键影响的药效团。

##### 3、方法：提出PC-DDI。首先通过RDKit等工具识别药物中的药效团，并提取组成原子、节点特征、边特征和空间坐标；然后以药效团为节点，为两个药物构建跨药物全连接的pharmacophore bipartite graph；在该图上提出Spatial Attention Weighted Graph Convolution Network（SAWGCN），同时根据节点语义相似度和药效团空间距离计算消息权重，更新药效团表示；随后聚合图级表示进行DDI二分类。为增强解释性，论文进一步引入受Granger因果思想启发的causal learning过程，通过扰动/比较不同药效团对预测结果的影响识别关键药效团。

##### 4、创新：

- **从pharmacophore功能单元重新定义DDI的结构表示。** 据作者表述，PC-DDI是其所知首个pharmacophore-based DDI prediction framework。与普通molecular graph或motif方法不同，PC-DDI把具有药理功能含义的pharmacophore作为基本节点，并构建跨两个药物的pharmacophore interaction graph，希望从“结构相似”推进到“功能单元如何相互影响”。这是论文最核心、最具有辨识度的贡献。

- **设计Spatial Attention Weight Graph Convolution Network（SAWGCN）。** 作者第二项贡献是将pharmacophore spatial information与node features共同纳入message passing，使graph representation不仅知道“功能类型是否相似”，还考虑药效团在单分子构象中的空间位置信息。其目的在于得到比纯拓扑/纯attention更完整的pharmacophore graph representation。

- **引入基于节点移除的causal inference过程识别关键pharmacophore。** 作者明确把这项方法作为第三项贡献，并称其用于识别对DDI具有causal influence的关键药效团。精确到方法层面，它受Granger causality启发，通过删除某个pharmacophore后prediction confidence的相对变化定义Importance Score，并迭代剪除低影响节点。我的理解是，这比单纯attention更接近功能依赖测试，但仍应谨慎区分“作者使用的causal inference表述”与严格统计因果识别。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看AAAI原论文模型图。）

##### 6、所用数据集：二分类（传导 + 归纳）

- D1：DrugBank 5.0.3。
- D2：Zitnik et al.构建的公开DDI/polypharmacy数据。
- D3：Lin et al. 2023公开DDI数据。
- D4：使用完整DeepDDI数据训练，测试集为DrugBank 5.0.5中新出现的DDI triplets。
- D5：使用完整DeepDDI数据训练，测试集为DrugBank 5.0.7中新出现的DDI triplets。
- 三种任务：Transductive = Known–Known；Inductive-S1 = Unknown–Unknown；Inductive-S2 = Unknown–Known。

##### 7、缺点/局限：药效团确实比普通频繁motif更具有功能解释，但“药效团”本身是规则定义的先验，并不保证对所有DDI机制都比BRICS/motif更优；构建跨药物全连接药效团二部图会引入大量实际并不发生相互作用的候选边。论文使用“causal”表述需要谨慎理解：其方法更接近基于预测变化识别功能重要性，是否满足严格因果推断假设仍需区分。空间距离来自单药构象，并不等价于两个药物在体内真实接触构象。

##### 8、个人评价（是否值得精读）：值得精读。药效团这个切入点在DDI方向相对新颖，尤其适合参考其药效团识别、特征构造和空间信息处理流程。需要带着批判性看待“更接近机制”这一结论：药效团比motif更具药理先验，但并不能自动保证预测机制真实。最有价值的延伸是把pharmacophore与pair-specific evidence、KG pathway以及counterfactual validation结合，而不是只换一个结构粒度。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- DDI结构学习：传统相似性方法 --> 分子指纹/子结构 --> 原子级GNN --> 精度提高，但可能关注不活跃片段，解释难对应生物功能。
- Pharmacophore：药效团描述产生药理活性所需的空间/功能特征 --> 相比普通motif更强调功能而非纯拓扑 --> 适合做DDI中的功能性基本单元。
- GNN解释/因果学习：attention只能说明模型权重 --> 不代表被关注结构对预测是必要的 --> 作者引入基于预测变化的causal learning思路识别关键pharmacophore。

##### 2、模型输入输出：

- 输入：DDI药物对的两个分子图以及交互标签；每个分子进一步被转换为药效团节点、药效团空间位置和相关边/原子特征。
- 输出：两个药物是否发生DDI的二分类预测；解释阶段输出对结果最关键的pharmacophore。

##### 3、关键模块（每个模块的功能）：

- 药效团识别与特征提取：识别每个药物的pharmacophore；通过RDKit获取组成原子、原子特征和空间坐标；药效团节点特征由组成原子聚合得到。
- 药效团空间位置：用组成原子的质心表示pharmacophore位置，为几何关系计算提供坐标。
- 药效团边/内部特征：聚合药效团内部相关原子键特征，形成统一edge-level描述。
- Pharmacophore Bipartite Graph：两个药物的药效团分别位于二部图两侧，跨药物药效团全连接，显式建模潜在pairwise functional interaction。
- SAWGCN：节点语义通过attention形成一组权重，同时根据两个药效团的欧氏距离形成空间权重，两者结合后控制邻居消息聚合。
- Graph-level Embedding：聚合更新后的pharmacophore node表示形成药物对/交互图的全局表示。
- DDI Predictor：通过注意力或MLP得到二分类概率，并以binary cross-entropy训练。
- Causal Pharmacophore Identification：比较关键药效团存在/被干预时的预测变化，寻找对模型输出影响最大的功能单元。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：D1–D5，具体构造见上。
- Baselines：DeepDDI、GAT、SSI-DDI、GMPNN-CS、DSN-DDI、PEB-DDI、SRR-DDI、HDN-DDI。
- 评估设置：D1和D3同时做transductive与inductive实验；D2做transductive；D4/D5专门测试更新DrugBank版本中新出现的interaction triplets。
- 评估指标：ACC、AUC-ROC、AP、F1；结果取5次重复实验平均值。
- 训练：100 epochs；learning rate 0.005；Xavier initialization；Adam；weight decay 0.005；batch size 1024；每个positive interaction生成1个negative sample。
- 消融：w/o SAGPooling、w/o self-attention、w/o SAWGCN，以及不同pharmacophore aggregation与fully-connected graph construction。
- 实验设备：论文致谢提到使用High-Performance Computing Center，但正文没有足够明确的具体GPU型号，Gold Note不做猜测。

##### 5、案例分析（做了什么样的案例）：

- 论文选取5组CYP3A4-mediated DDI pairs做case study，分析抑制剂/诱导剂对应的关键pharmacophores是否与已知代谢机制一致。Figure 5把key pharmacophore atoms标红、完整pharmacophores标绿；正文进一步讨论Clarithromycin通过macrolide ring抑制CYP3A4、Lenvatinib芳香环作为主要结合位点，以及Diltiazem、Ketoconazole、Phenytoin、Rifampicin等药物与CYP3A4/PXR相关的功能结构。作者据此说明模型识别的pharmacophores与已知biology相符。需要保持边界：这种一致性 + node-removal重要性比纯attention更强，但仍不是随机化临床/实验层面的因果证明。

##### 6、关键启发（哪些地方对自己有用）：药效团的识别和特征处理流程非常值得借鉴，尤其是把functional type和spatial coordinate同时作为结构表示。对于自己的方向，不必直接接受“pharmacophore一定优于motif”，可以把BRICS motif、pharmacophore和learned substructure作为三种候选粒度做统一比较；更进一步，利用药物对co-attention动态选择关键pharmacophore，再用KG机制原型解释这些功能单元为何会导致特定DDI事件，并通过双层反事实干预验证结构证据和机制证据。
