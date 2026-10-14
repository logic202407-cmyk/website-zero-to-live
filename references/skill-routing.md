# 技能与方法组合

skill是方法包，CLI/API/浏览器是执行通道，AGENTS是仓库约束，账号/密钥是访问条件；安装skill不会自动获得其他三者。

先看本次环境公布的能力和项目约束，再选择。不要硬编码原作者本机路径、代理品牌、模型或账号；没有第三方skill也应按本包内置参考完成工作。

| 阶段 | 有条件时采用 | 缺少时的内置方法 |
|---|---|---|
| 需求与产品 | product-design等，任务确实需要时 | 简报＋主旅程＋可观察完成标准，见architecture/build |
| UI上下文路由 | ui-skills-root | 根据具体任务选择一个设计方法，不批量加载技能 |
| 主视觉与交互 | Impeccable或适合框架的frontend-design | 内容层级、token、组件状态、桌面/手机截图，见design |
| React/Next评审 | Vercel react-best-practices | 服务端权限、共享状态、数据读取、缓存、性能，见build/data-ai |
| 界面可访问性评审 | Vercel web-design-guidelines | 键盘、焦点、标签、错误关联、对比度与窄屏流程，见design |
| 细节动效 | emil-design-eng、apple-design，选择相关的一项 | 即时反馈、可中断、克制动效、reduced-motion |
| 独立HTML原型 | web-design-engineer | 快速可交互原型；迁产品时重建为项目正式组件和构建 |
| 门户专门问题 | lab-portal-site-building | 仅提取适用的内容管理/安全方法，不覆盖当前账号模型 |
| 数据和认证 | Supabase官方skill及Postgres指南 | schema/迁移/会话/访问矩阵/真实A-B隔离，见data-ai |
| 视觉素材 | imagegen或已授权设计工具 | 有许可的现成素材或CSS/矢量；不得捏造真实产品截图 |
| 浏览器验证 | 可用浏览器自动化/Playwright | 若工具缺失则给可执行步骤并标未验，不假称已看截图 |
| 技能维护与分发 | skill-creator | frontmatter、相对引用、行为场景和安装包一致性验证 |

不同时叠加多套互相冲突的审美体系。用户指定的技能优先，仓库指定的必需视角按要求执行；每次实际加载遵守它的SKILL.md。检查技能内容不等于执行了技能。

## 来源与可移植性

可按任务选用Impeccable视觉方法、ui-skills-root路由、Vercel评审技能，以及apple-design、emil-design-eng、web-design-engineer、lab-portal-site-building等资源。安装记录不代表已经执行过评审或验收；实际使用时记录选择、版本和结果。本技能仅介绍方法，不分发第三方技能原文或资产。

安装第三方技能前核对官方来源、版本/commit、许可证和脚本作用；未发现就明确缺失。不要凭名称猜下载地址，不把运行缓存当安装目录。Vercel评审技能不要求网站部署到Vercel。原型里的CDN/Babel模式不直接移入正式产品构建。

多人分工可按“产品与契约、实现、视觉、复核、发布负责人”分配；只有获得协作授权才启动其他代理。角色不绑定特定工具品牌，具备相应能力的代理或人类团队都可执行本流程。
