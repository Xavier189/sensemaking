# 方法参照与取舍

以下为 2026-11-03 至 2026-11-11 对上游 `main` 分支指令、官方文档与相关论文的核验与设计取舍，不是效果排名或运行基准。借鉴方法，未将第三方 Skill 包或执行流程作为依赖引入。

| 参照 | 吸收 | 不吸收 |
|---|---|---|
| [Matt Pocock grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) | 根据决定依赖按轮推进问题前沿（frontier）；每题附推荐答案；事实由 Agent（或独立上下文）调查 | 必须遍历设计树全部叶节点才算完成；统一要求用户确认后才允许进入下一步行动 |
| [Matt Pocock domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) | 对照代码检验描述；用具体场景发现概念边界 | 每次明确术语就写词汇表；把讨论默认变成文档维护 |
| [Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | 相关上下文先行（Look Before You Ask）；信息齐全的小任务直接执行；比较方案及代价；Agent 自决的细节标为自身选择（your call）而非用户已同意 | 除非用户主动声明跳过提问，否则非琐碎改动一律强制先发独立方案消息、写并提交 `docs/superpowers/specs/` 设计文档、获批后再固定转调 `writing-plans` |
| [GSD assumptions mode](https://github.com/gsd-build/get-shit-done/blob/main/docs/workflow-discuss-mode.md) | 先分析代码，展示假设的证据、错误后果与不确定性，便于用户纠正 | 固定文件数量、阶段目录与输出文档；将现有实现当成用户期望 |
| [Spec Kit clarify](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md) | 按影响与不确定性处理覆盖缺口；更新矛盾陈述；问题说明意义并附推荐选项 | 规格文件前置、固定问题与答案长度、将设计方法完全排除在讨论之外 |
| [Requirements Clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) | 核对价值并寻找更简单的实现 | 主观清晰度分数作为完成标准；默认生成 PRD；出现代码或路径就不触发 |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack)（`cursor/plugins` 仓库中的个人工作流，作者 poteto；访问于 2026-11-04） | 首条回复复述目标与问题且不等待确认；两次同前提修复失败后直接验证前提（Attack the Premise）；能运行观察的分歧用一次性原型判定、不把可运行的检查交给用户；用户先别说出原因猜测以免收窄搜索（转为 Agent 先独立推导）；`/sharpen` 的专业做法、原始材料、方法工具与外部检验四问；`/blast-radius` 的证据等级 | 23 个 playbook 原样抄入 todo 的固定流程；回复中必须点名引用原则；默认多模型 arena/swarm；可逆工作默认不询问直接推进（与用户保留关键拍板权的选择冲突）；不提供可照打回复简写的做法（本项目在说明选项含义后保留附条件推荐项与简短确认） |
| [gstack](https://github.com/garrytan/gstack)（`/office-hours` 与 `/plan-ceo-review`，访问于 2026-11-11） | 围绕真实需求现状、具体触发情境与最小切口（narrowest wedge）核验原始想法，避免泛泛罗列点子 | `/plan-ceo-review` 默认寻找“10 星产品”诱导范围扩张；强制落盘 `~/.gstack/` 设计文档并串入 23 个固定角色流水线 |

## 行业实践与学术依据

以下资料于 2026-11-03 至 2026-11-11 核对一手来源，仅保留在内部维护文档中，不注入运行时 Skill 上下文：

| 议题与来源 | 核心发现与适用边界 | 设计落点 |
|---|---|---|
| **上下文供给、文档泥球与指令句式合规**<br>[Anthropic `claude-api/shared/prompt-audit.md`](https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/prompt-audit.md) 与 [`model-migration.md`](https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/model-migration.md)（访问于 2026-11-04）；[*Claude Code: Best practices for agentic coding*](https://web.archive.org/web/20250420034405/https://www.anthropic.com/engineering/claude-code-best-practices)（2025-04-18 发布，Wayback 存档）；[Birgitta Böckeler 对 SDD 工具的实测分析](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)；[Evaluating AGENTS.md (arXiv:2602.11988)](https://arxiv.org/abs/2602.11988)；[Do Coding Agents Follow AGENTS.md? (arXiv:2611.04367)](https://arxiv.org/abs/2611.04367) | Anthropic 的 prompt 审计文档指出：新模型更字面地遵循指令，全大写强调、`CRITICAL/MUST` 堆砌会导致过度触发与僵硬行为；为判断型任务写 step-by-step 编排会压过模型自己的规划；同一信息散落多处会各自漂移，应“只放在一处”。Böckeler 实测指出，重型 SDD 工具会把小修复膨胀为 4 个 user story 与 16 条验收标准，或生成大量需人工审阅的 Markdown。ETH Zurich（arXiv:2602.11988）在 SWE-bench 与 AGENTbench 上实测显示，冗长的仓库级上下文文件使推理成本上升逾 20%，LLM 生成的概览文件还会轻微拉低任务成功率；Tsuchida 等（arXiv:2611.04367）测得复杂嵌套条件句比直接祈使或带理由陈述的规则合规率低 14–56 个百分点 | 用平直短句要求实质实现前核对期望结果、边界与成功证据；同一规则在 SKILL.md 内只写一处，reference 文件只做展开与指针；把仓库内的说明文档、注释和 `AGENTS.md` 视为待与实际代码核对的主张；默认在对话上下文维护轻量决策状态（`STRUCTURE`），面临上下文自动压缩时输出紧凑内联摘要，不把重型静态 PRD/Spec 作为必经门禁 |
| **错误前提下的顺从偏见、抗压校准与用户自主权**<br>[EGDP (arXiv:2607.10411)](https://arxiv.org/abs/2607.10411)；[Thinking-in-Bets (arXiv:2610.34654)](https://arxiv.org/abs/2610.34654)；[Big-Big-SycoBench (arXiv:2610.15634)](https://arxiv.org/abs/2610.15634)；[Claude Constitution — Autonomy](https://www.anthropic.com/constitution) | EGDP 在 code smell 检测上显示，带错误前提的提示会使判断翻转率（DFR）达 72%、错误顺从率（FAR）超 90%，先提取代码证据可将 DFR 降至 12%、FAR 降至 21%；实验对象为 Qwen2.5 等小模型，数值不能直接外推到前沿模型。Big-Big-SycoBench 把“对有效论据的响应率”与“对无效论据的顺从率”分开度量：无效论据顺从率在 OpenAI 系列内从 GPT-4o 的 95% 降到 GPT-5 的 57%、GPT-5.5 的 22%、GPT-6 Astra 的 0.2%，而 Opus 5.5 对有效论据的响应率只有 32%（100 件子集）——对新一代模型，“听到有效反证仍不更新”与“屈从无效施压”同样是现实失败。Thinking-in-Bets 的 Always-On 条件在多个模型上显著减少了收到反馈后的错误改口（false reversals）；其机制是在反馈到来前先绑定论断与验证依据，而非笼统“坚持立场”。Claude 宪法 Autonomy 条款的原文是：对不赞同的修法可以说出顾虑，但仍应尊重用户意愿并按其要求去修——原文没有再确认一轮 | 将用户给定的根因判断与指定改法视为待核验假设：证据支持且边界清晰时直接推进；证据矛盾时说明真实机制并转向；证据不足时标明未核实并给出最小验证步骤。用户看过矛盾证据后仍在自身范围内坚持可逆改法时，在同一回复中说明未解决问题与附加风险后随即照办并留痕，只有风险尚未展示或改动难回退时才等确认。坚持与新证据分开处理：用户带来改变机制的材料时据此重新推导，评测中用一个新证据回合专门检验这一方向 |
| **选择性主动澄清与演进需求收敛**<br>[ClarifyGPT (arXiv:2310.10996)](https://arxiv.org/abs/2310.10996)；[Ask or Assume (arXiv:2603.26233)](https://arxiv.org/abs/2603.26233)；[Orchid (arXiv:2604.21505)](https://arxiv.org/abs/2604.21505)；[ClarifyCodeBench (arXiv:2607.00711)](https://arxiv.org/abs/2607.00711)；[CONTRA (arXiv:2610.01769)](https://arxiv.org/abs/2610.01769)；[FeatureLoop (arXiv:2610.35488)](https://arxiv.org/abs/2610.35488) | Orchid（1,304 个含词法、句法、语义与模糊四类歧义的任务）显示欠规范要求普遍令模型静默产出分叉代码；ClarifyCodeBench 以 TKQR（关键问题是否尽早问出）与 ORA（提问轮数是否接近最优，多问少问都受罚）度量澄清质量；Ask or Assume 在欠规范 SWE-bench Verified 上，单 agent 每轮自检缺口只达 61.2%，独立检测器约束主 agent 时达 69.4%（完整规范为 70.8%），原因是单 agent 常在察觉缺口前已开始改代码；CONTRA 通过检查不同候选答案是否导致程序在共享输入上的执行行为差异来筛选问题；FeatureLoop（61 个跨 34 仓库的持久工作区任务）表明真实开发会在中间产物后持续引入需求变更与完成反馈 | 保留显式的澄清判断规则：可查事实由 Agent 调查，局部可逆细节自行决定；仅当至少存在两个合理答案且会实质改变目标、可观测行为、验收依据或难逆转承诺时才提问，宿主结构化多选控件仅在主会话用于后果已讲清的有界选项。“进入实质实现前”的核对作为首次编辑前的独立检查动作；实现中途需求变更时废止旧决定并同步更新已改代码与验证，避免残留过时分支 |

## 组合后的原则

调查、解释、对话和设计可以交错。先在相关上下文中发现值得讨论的影响，再由事实、知识缺口、用户选择或验证需求决定下一步动作。

需求清楚不是跳过核验的理由；已经核验的前提也不因新消息而重复讨论。分析发现须关联当前目标，独立优化不得自动变成实施要求。

现有 Discover 的多种方向与具体例子、Clarify 的依赖感知提问、Challenge 的有依据判断和 STRUCTURE 的状态保留继续使用。主入口不再要求先识别某种不确定性或可见缺陷才能开始。

上述取舍需要通过真实风格输入和隔离 fixture 验证。热度、指令长度和方法数量不能证明触发可靠或结果更好。
