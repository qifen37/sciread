# 快读笔记

##### 1、论文标题：Multi-Relational Contrastive Learning Graph Neural Network for Drug-Drug Interaction Event Prediction（用于DDI事件预测的多关系对比学习图神经网络）

##### 2、研究问题：现有GNN类DDI事件预测方法往往只利用其中一类信息：一部分方法强调单药分子结构，却忽略药物之间已知的多关系DDI网络；另一部分方法建模药物交互网络，却弱化了每个药物内部的分子结构。同时，DDI事件类别高度长尾，稀有事件缺少足够训练样本，普通监督学习容易偏向高频事件。MRCGNN因此希望同时融合“intra-drug molecular structure”和“inter-drug multi-relational interaction”，并利用对比学习从少样本事件中学习更稳健的关系表示。

##### 3、方法：提出MRCGNN。首先使用分子图编码器从每个药物的原子-键图中提取结构特征，并以这些结构特征作为药物节点属性构建多关系DDI事件图；随后在该多关系图上进行GNN消息传播，联合学习药物结构和不同事件关系；为缓解稀有事件数据不足，模型进一步设计Multi-Relational Graph Contrastive Learning，并提出Dual-View Negative Counterpart Augmentation，为不同关系构造对比视图，使同类关系/药物表示在表示空间中更稳定，最终用于多类别DDI事件预测。

##### 4、创新：

- **统一药物结构信息与药物交互信息。** MRCGNN首先从drug molecular graphs提取药物结构特征，再把这些特征作为节点属性注入multi-relational DDI event graph，并在该图上进行关系感知消息传播。作者针对的是一个非常具体的缺口：已有GNN方法常常只保留drug structural information或drug interactive information中的一类，而MRCGNN试图在同一表示框架中联合两者。

- **提出面向多关系DDI图的Graph Contrastive Learning。** 模型不是直接套用普通节点级contrastive learning，而是针对multi-relational DDI event graph设计对比目标，使表示学习显式保留不同事件关系下的结构信息，为多类别DDI event prediction提供额外自监督信号。

- **设计Dual-View Negative Counterpart Augmentation以挖掘rare DDI events。** 作者通过两类负向counterpart视图对节点特征与关系结构进行扰动，并用multi-relational contrastive objective从标签极少的事件中提取隐含信息。这里真正的创新点是“针对relation-level long-tail设计对比增强”，而不是泛泛地把contrastive learning加入GNN。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看原论文整体框架图。）

##### 6、所用数据集：多分类DDI事件预测

- Deng’s dataset：37264条DDIs、570种drugs、65类DDI events。
- Ryu’s dataset：191570条DDIs、1700种drugs、86类DDI events。
- 作者按每个事件的frequency把类别分为5组，并将频次位于[1,10]的事件定义为rare events，分别评估all events和rare events。

##### 7、缺点/局限：MRCGNN在2023年的创新点比较明确：把多关系图和对比学习结合到DDI长尾问题中。但它仍然把每个药物压缩为一个节点表示后在DDI图上传播，Drug A与Drug B之间具体哪些子结构相互作用并没有显式建模；对比增强能够改善稀有类别表示，却不直接等价于机制解释。标准随机划分下同一药物可能同时出现在训练和测试中，因此结果不能自动外推到完全新药的cold-start场景。

##### 8、个人评价（是否值得精读）：值得精读，尤其适合研究多分类DDI、类别不平衡和关系级对比学习。它是“结构信息 + 交互网络 + contrastive learning”三者结合得比较干净的一篇。对后续工作最有价值的是其长尾问题意识和relation-aware contrastive objective；如果进一步加入pair-specific子结构交互、机制原型或cold-start评估，会比原框架更完整。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- 分子结构路线：GNN直接编码单药molecular graph --> 能学习原子/键结构，但忽略药物之间已知事件网络中的高阶关系。
- DDI网络路线：把药物作为节点、DDI事件作为多关系边 --> 能学习事件关系，但如果节点初始特征弱，就难以表示药物本身结构。
- 长尾问题：65/多类DDI事件频次差异明显 --> 稀有事件样本不足 --> 普通交叉熵更偏高频类 --> 引入multi-relational contrastive learning增强少样本事件。

##### 2、模型输入输出：

- 输入：每个药物的分子图，以及训练集中的多关系DDI事件图。
- 输出：给定药物对所属的DDI事件类别。

##### 3、关键模块（每个模块的功能）：

- Molecular Graph Encoder：从原子、化学键等局部结构中提取每个药物的结构表示，为DDI图提供具有化学意义的节点属性。
- Multi-Relational DDI Event Graph：把药物设为节点、不同DDI事件设为不同relation type，显式保留事件类别语义。
- Multi-Relational GNN：在多关系图上进行消息传播，使药物表示同时吸收结构初始特征和邻接药物/关系信息。
- Contrastive View Construction：围绕原多关系图构造多个增强视图，为关系级对比学习提供正/负样本。
- Dual-View Negative Counterpart Augmentation：构造两种负向counterpart视图，避免普通随机扰动过弱，并让稀有关系也能获得额外训练信号。
- Multi-Relational Contrastive Loss：约束原图与增强视图中的关系/节点表示，提高跨视图一致性和类别可分性。
- Event Classifier：将药物对表示输入分类器，预测最终DDI事件类型。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：
  - Deng’s dataset；
  - Ryu’s dataset。
- Baselines：DeepDDI、SSI-DDI、TrimNet-DDI、MUFFIN、R-GCN、GoGNN等结构或图关系方法。
- 评估指标：ACC、Macro-F1、Macro-Recall、Macro-Precision，并额外分析rare/fewer事件类别表现。
- 公开复现仓库提供Deng和Ryu数据以及5次重复训练脚本，主实验以多次运行平均表现为基础。
- 实验设备：官方代码仓库主要提供环境和执行脚本，Gold Note不对未明确报告的GPU做猜测。

##### 5、案例分析（做了什么样的案例）：

- 论文的重点案例不是具体药物机制，而是按照事件频率拆分common/rare类别，分析对比学习对低频DDI事件的提升。该分析用于证明Dual-View和multi-relational contrastive objective并非只提高整体ACC，而确实改善了长尾类别识别。

##### 6、关键启发（哪些地方对自己有用）：对于多类别DDI，不能只看总体ACC，应该把rare event作为独立研究问题。可以借鉴MRCGNN的relation-aware contrastive思路，但把contrastive unit从整药节点推进到“药物对-子结构-机制原型”层面，例如对同一事件类别的关键子结构证据做一致性约束，并对不同事件原型做分离。另外建议把长尾实验与cold-start结合，因为真实的新药+稀有事件往往同时出现，单独解决class imbalance还不够。
