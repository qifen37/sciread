# SciRead 质量 Rubric

该文件整合事实准确性、创新忠实度、批判性阅读和笔记质量要求。

## 1. 事实准确性
高质量笔记必须：
- 只写来源支持的事实；
- 缺失信息保持缺失；
- Dataset / Task / Split 以当前论文为准；
- 不把相关论文的协议串进来。

## 2. 研究问题
必须讲清：
- 现有范式；
- 具体不足；
- 为什么重要；
- 本文如何重新定义或解决。

## 3. 创新忠实度
“创新”必须：
- 对应作者 contribution；
- 解释技术上哪里新；
- 说明解决哪个 limitation；
- 区分方法创新与实验结果；
- “first” 保留作者限定。

## 4. 方法完整度
主要模块写清：
- 目的；
- 输入；
- 操作；
- 输出；
- 与整体 pipeline 的关系。

## 5. 实验忠实度
正确对应：
- Dataset；
- Task；
- Split；
- Baseline；
- Metric；
- Backbone；
- 仅在论文明确报告时写 Implementation / Hardware。

## 6. Case Study
如果存在，保留：
- 起始 query / 状态；
- 中间证据或推理；
- 最终结果；
- 它真正验证了什么。

如果不存在，就明确写没有。

## 7. 强 Claim 校准
### Causal
检查 Intervention、Deletion、Counterfactual、Treatment/Control 或正式因果识别。Attention 不能直接叫因果。

### Mechanism
判断机制是显式、有监督、Prototype/Pathway/Relation、Latent、Retrieved，还是隐式。

### Faithful
更强证据包括：Deletion、Sufficiency/Necessity、Counterfactual、Prediction Sensitivity。

### Biological Grounding
区分：
1. 合理生物学叙事；
2. 数据库关系；
3. 文献支持机制；
4. 实验验证。

## 8. 科研迁移价值
“关键启发”应给出可执行的研究操作，而不是泛泛夸奖。

## 9. 信息密度
要足够详细，但不重复。

仅仅格式正确，不代表笔记质量高。

## 10. 50 分建议评分
- Research Problem：0–5
- Method Pipeline：0–5
- Contribution Fidelity：0–5
- Module Detail：0–5
- Experiment Fidelity：0–5
- Case Study：0–5
- Critical Analysis：0–5
- Research Transfer：0–5
- Information Density：0–5
- Factuality：0–5

45–50：Gold 质量  
40–44：强  
34–39：可用但不完整  
25–33：过度压缩 / 有重要遗漏  
<25：较差
