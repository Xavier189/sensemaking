# 行为校准

[`evals/evals.json`](../../evals/evals.json) 是当前唯一保留的 eval manifest。逐次模型输出、评分页面和阶段 benchmark 不属于产品事实，也不应占据文档导航；运行结果应进入 CI artifact、release evidence 或外部实验记录，而不是长期堆在仓库。

## 覆盖面

- Discover：无方向、缺判断基础、避免单一 hypothesis 锚定；
- Clarify：solution-disguised-as-requirement、evidence gate、owner decisions；
- Challenge：非代码方案、material defect、finding-first；
- STRUCTURE-only：修订状态、handoff 与普通转换的边界；
- Skip：机械一步任务、行为保持的局部 refactor、相关前提与影响已核验的执行任务；
- Fact uncertainty：性能根因与外部事实先调查；
- Invariance：相同 thinking state 跨代码/非代码、个人/工作、greenfield/maintenance 保持同一路由；
- Design：按需形成适量设计，不自动开启 plan、reviewer 或未授权 implementation。
- Discussion：短草案与源码共同输入，调查后回到讨论，推荐随目标与取舍变化；
- Continuation：“继续”延续当前活动，局部回答不确认其他建议，不扩大授权；
- Authorization：已授权执行在检查完成后继续，无需重复确认。
- Completion：同一份有缺陷方案中，审查意见交付、共同定稿与已授权修订有不同完成条件；开放选择不自动变为确认或风险接受。
- Readiness：肯定语气下的范围遗漏、完整验收中的代理指标、依据充分时直接实现；解释进场依据不能成为额外批准环节。用户明确委托选择与仅表示不知道应区别处理。

新增上下文用例覆盖：完整功能描述与现有机制、事件乱序造成的隐含依赖、一句话 Bug、错误诊断前提的证据纠偏、无新证据的二轮坚持（说明后照办并留痕）与带新证据的三轮改判（据新材料重新推导而非维持原评估）、正确诊断的直接确认执行、同前提多次修复失败后的前提复核、非代码协作影响、同源狭窄事实查询、已核验执行、先解释再选择、跨轮纠正与未决项。描述长度与文件位置不作为跳过依据。

## 执行约定

`files` 使用仓库相对路径。每次运行先把这些 fixture 复制到隔离的临时目录，保留输入文件之间的相对关系，并向 agent 提供副本路径。fixtures 是虚构的评测输入，不代表任何生产项目。不得让实现用例修改仓库原件或用户项目。

带 `follow_up_turns` 的用例按顺序运行：发送首个 `prompt`，保存完整回答与工具轨迹，再逐轮发送后续 `prompt`。同一用例内保留会话；不同用例、baseline 与 candidate 使用各自的 fresh context。后续输入按原文发送，不补充期待答案；若它与模型的问题没有自然衔接，记录该限制。

`invocation: explicit` 的用例使用指定版本的 Skill；`invocation: implicit` 的用例只提供技能目录中的 name/description 与可读取路径，由 host 决定是否加载。不得把完整正文预先注入隐式触发测试。旧用例未标 invocation 时用于行为校准，不据此计算隐式触发率。

评分应同时查看对话、读取/写入工具轨迹和文件差异，分别报告：

- **触发**：在隐式场景中是否选择并加载 Skill；
- **作用**：是否依据材料发现影响结果的遗漏或假设，推荐是否受真实前提约束；
- **开始依据**：进入实质实现前，是否在用户能读到的回复正文里、第一次编辑之前，用实际材料简述期望结果、验证办法和关键假设；检查验证是否对应目标，不能只匹配“需求清楚”等字眼，工具调用之间的进度笔记不算；
- **连续性与授权**：是否正确保留未决项、当前活动和允许修改的范围。

提问数量不是质量指标。明确请求可零提问；过早定论、虚构事实或问题、重复建议已有机制、无授权写入均需单独记录。运行结果区分静态检查、行为 smoke test 与多次重复的 benchmark；单次对照不能证明触发率或整体质量提高。

对于审查用例，同时检查是否已交付可用的意见，以及是否把非必要确认作为交付前置条件；不能因回答含有一个真实 owner question 就判失败。对于 Discover，检查是否提供了有意义的选择依据，不能只计数方向或问题。implicit 用例需包括相近措辞的清晰执行与事实查询，避免只验证正例。

## 静态校验

```bash
uv run --no-project python -m json.tool evals/evals.json >/dev/null
uv run --no-project --with pyyaml python /path/to/skill-creator/scripts/quick_validate.py skills/sensemaking
```

行为 benchmark 必须记录 model、host instructions、skill path、run count、grader 与原始 evidence。被全局 instructions 或 memory 污染的 baseline 不能解读为裸模型对照；缺失的 timing/token 数据不得填零后用于效率结论。
