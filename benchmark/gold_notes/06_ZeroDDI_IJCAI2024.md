# 快读笔记

##### 1、论文标题：ZeroDDI: A Zero-Shot Drug-Drug Interaction Event Prediction Method with Semantic Enhanced Learning and Dual-Modal Uniform Alignment（ZeroDDI：基于语义增强学习与双模态均匀对齐的零样本DDI事件预测）

##### 2、研究问题：绝大多数多分类DDI模型默认训练阶段已经见过所有DDI事件类别，但现实中可能不断出现新的interaction event，而这些新事件类别在训练时没有任何标注样本。这个问题不同于“新药cold-start”：ZeroDDI关注的是unseen DDI event classes。作者指出零样本DDI事件预测面临两个关键困难：一是如何构造具有生物学区分度的事件语义表示，使未见类别也能通过文本/语义与药物对建立联系；二是DDI事件本身高度不均衡，已见类别的长尾分布会让结构表示与语义空间对齐进一步偏斜。

##### 3、方法：提出ZeroDDI，将药物对结构模态与DDI事件语义模态映射到共享空间。首先利用事件文本描述和BioBERT等生物医学语言模型获得事件语义，并通过Biological Semantic Enhanced DDIE Representation Learning突出关键生物学语义、蒸馏与分子子结构相关的判别信息；随后编码药物对结构表示；最后提出Dual-Modal Uniform Alignment，将drug-pair representation与event semantic representation都约束在单位超球面上，并同时进行均匀分布和匹配对齐，使已见/未见类别的语义原型都能参与相似度分类，从而完成ZS-DDIE与GZSL预测。

##### 4、创新：

- **提出Zero-Shot DDI Event Prediction这一新的任务设定，并构建对应数据集。** 这是作者明确列出的第一项贡献：传统DDIE方法默认所有事件类别在训练中可见，而ZeroDDI研究的是unseen DDIE classes没有任何训练样本的场景。作者不仅提出ZeroDDI方法，还基于DrugBank v5.1.9人工标注DDIE attributes，构建ZS-DDIE benchmark。因此这里的“zero-shot”核心是**未见事件类别**，而不是未见药物。

- **设计Biological Semantic Enhanced DDIE Representation Learning（BRL）。** 作者从class-level文本语义和attribute-level语义两个层面表示DDIE，并利用molecular substructure与文本token之间的细粒度交互指导bi-level semantic fusion，目的是蒸馏与分子结构相关的判别语义，使不同事件类之间的语义距离更符合生物学关联，从而让seen→unseen知识迁移成为可能。

- **提出Dual-Modal Uniform Alignment（DUA）缓解零样本DDIE中的类别不平衡。** DUA同时约束drug-pair structure representations与DDIE text representations在unit sphere上更均匀地分布，并对匹配的drug pair–event表示进行alignment。作者的核心出发点不是普通跨模态对齐，而是利用uniformity改善长尾类别造成的不清晰decision boundary，提升unseen class discrimination。

- **通过CZSL/GZSL和新版本DrugBank应用分析验证实际zero-shot能力。** 作者把实验有效性作为第四项贡献，并进一步使用DrugBank v5.1.11中后来出现的6个新DDIE进行application analysis，说明其任务设定不仅是人为拆分。

##### 5、模型图：

（Gold Benchmark不内嵌原论文图片，建议查看IJCAI原论文模型图。）

##### 6、所用数据集：零样本/广义零样本多分类DDI事件预测

- 基于DrugBank v5.1.9构建ZS-DDIE dataset：2004种approved drugs、394118条DDIs、175种具有唯一文本描述的DDIE。
- 事件语义进一步标注为2类Signs、3类Patterns和114类Effects等attribute-level text。
- 按事件频次将107个DDIE设为seen classes、68个DDIE设为unseen classes；drug pair是asymmetric的，即两个药物在事件中的角色不可随意交换。
- 同时评估Conventional ZSL（CZSL）和Generalized ZSL（GZSL）；CZSL对unseen classes做3-fold validation/test划分。

##### 7、缺点/局限：ZeroDDI的任务定义很有价值，但它依赖事件文本/语义质量，未见类别如果描述过于相似或缺乏明确生物语义，映射难度会显著增加；结构模态最终仍被压缩为药物对向量，事件语义与具体子结构之间的对应关系不够显式。Dual-Modal Uniform Alignment能够缓解分布不均衡，但“均匀”是表示空间正则，并不等于解决真实生物学类别长尾。此外，ZSL unseen event与新药inductive是两个独立维度，论文主要解决前者。

##### 8、个人评价（是否值得精读）：值得精读。ZeroDDI的最大价值不只是某个alignment loss，而是把DDI任务从“已知标签分类”推进到“未见事件类别识别”，这对多类别DDI非常有启发。对于自己的工作，可以进一步考虑双重zero-shot：既有unseen drug，又有unseen event；或者把event semantic prototype替换为知识图谱机制原型，使事件语义从纯文本空间转向可验证的机制空间。

---

# 精读笔记

##### 1、研究背景（相关工作空白、动机）：

- 传统DDIE多分类：训练/测试共享固定事件标签集合 --> 对已见类性能不断提升 --> 现实中新DDI机制或事件不断出现 --> 对没有训练样本的新类别无能为力。
- Zero-shot learning：通过类别语义描述把unseen class映射到共享表示空间 --> 在DDI中事件文本具有药理语义，但原始标签描述可能含噪、过于表面 --> 需要生物语义增强。
- 类别不平衡：DDI事件频率长尾严重 --> seen classes内部就存在强不均衡 --> 简单跨模态对齐容易被高频类主导 --> 需要uniformity约束降低表示坍缩和偏置。

##### 2、模型输入输出：

- 输入：药物对的分子结构/结构表示；每个DDI事件类别对应的文本语义描述。
- 输出：ZSL设置下预测药物对属于哪个未见DDI事件；GZSL设置下在seen + unseen事件集合中联合分类。

##### 3、关键模块（每个模块的功能）：

- Drug Pair Structural Encoder：编码两个药物的分子结构并形成pair representation，为跨模态匹配提供结构侧表示。
- DDIE Text Encoding：使用生物医学预训练语言模型对事件描述进行编码，将离散event ID转化为连续语义向量。
- Biological Semantic Enhancement：强化与药理机制相关的关键词/语义，并抑制与分类无关的表面文本信息。
- Molecular Substructure-related Semantic Distillation：从事件语义中提炼与分子局部结构有关的判别信息，使语义模态更容易与结构模态对应。
- Dual-Modal Uniformity：分别约束drug pair和event semantic embedding在unit sphere上的分布，使类别和样本不集中在少数高频方向。
- Cross-Modal Alignment：拉近匹配的药物对-事件表示，并拉开不匹配类别，实现seen-to-unseen知识迁移。
- ZSL/GZSL Inference：根据共享空间中的相似度选择最匹配事件原型，无需为unseen event提供训练样本。

##### 4、实验设置（数据集、Baselines、评估指标、实验设备）：

- 数据集：DrugBank v5.1.9构建的ZS-DDIE benchmark，107 seen / 68 unseen event classes。
- Baselines：
  - 3DGT-DDI：修改其分类头以适配ZS-DDIE；
  - ZSLHinge；
  - ZSLCE；
  - ZSLTriplet；
  - 同时比较attribute-based与class-text-based semantic representation。
- 评估场景：
  - CZSL：测试只包含unseen classes；
  - GZSL：测试同时包含seen与unseen classes。
- 评估指标：CZSL使用Top-1/Top-3/Top-5 Accuracy及unseen classes平均Top-1 accuracy；GZSL进一步分别评价seen/unseen性能和二者平衡。
- 实现：官方代码基于PyTorch 1.11、PyG 2.1、RDKit、Transformers等，并使用BioBERT checkpoint。
- 实验设备：论文/官方README没有足够明确的信息支持在Gold Note中写具体GPU型号，因此不做猜测。

##### 5、案例分析（做了什么样的案例）：

- 论文除了embedding distribution可视化，还专门做了Zero-Shot DDIE Application Analysis：作者以DrugBank v5.1.9为Existing Dataset，以后续DrugBank v5.1.11为Novel Dataset，发现其中存在6个由既有attributes组成、但在旧版本中没有出现过的DDIE；随后直接用旧数据训练ZeroDDI去预测这些新事件，在没有对应训练标签的条件下获得61.11%的平均准确率。该实验用于验证“unseen event class确实会在数据库更新中出现”，比纯随机hold-out更接近论文想解决的实际问题。

##### 6、关键启发（哪些地方对自己有用）：ZeroDDI可以直接启发“机制原型”方向：把每个DDI事件不仅看成label，而看成一个可表示、可比较的mechanism prototype。进一步可以用DrugBank事件描述、KG relation cluster、路径语义共同定义prototype，再让药物对通过子结构证据去选择原型。另一个很重要的启发是区分三种泛化：unseen pair、unseen drug、unseen event。未来论文如果能同时覆盖这三个轴，会比只做某一种cold-start更有说服力。
