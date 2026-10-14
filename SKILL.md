---
name: website-zero-to-live
description: "Build and launch a personal website from a resume, portfolio, project notes, or a short introduction. Use when a user wants a personal site, job-search portfolio, resume website, or AI-assisted website creation through preview, domain purchase, DNS, HTTPS, deployment, and handoff. 适用于秋招求职、个人主页、作品集、简历网站及从零建站上线。For an existing site, continue its current implementation."
metadata:
  version: "1.1.0"
---

# Personal Website Launch

帮助用户用 AI 快速打造并上线自己的个人网站。优先交付可以公开访问、展示真实经历与作品的网站；根据目标岗位组织内容，让技术与非技术岗位的求职者都能使用。

## When to Use

- 用户想做个人主页、求职作品集、简历网站或个人品牌网站。
- 用户希望将已有简历、项目笔记、设计稿、运营案例或写作成果整理为网站。
- 用户要求从想法推进到预览、域名购买、正式上线与后续维护。
- 用户已有网站，需要继续实现或上线；保留既有框架和工作成果。

单个文案或组件修复不启动整套建站流程。其他类型网站仍可使用通用参考，但不要向个人展示站默认添加账号、数据库、支付或聊天机器人。

## Prerequisites

读取当前目录、适用 AGENTS.md、Git状态和已有实现。确认代理实际可用的文件、终端、浏览器与发布能力；缺少工具时准确记录可执行范围。

确认用户希望公开的资料、目标读者/岗位、风格偏好、已有作品与域名、预算、发布授权。先整理公开内容和完成本地实现；账号登录、验证码或付款条件缺失时继续不依赖它的工作。

## Quick Decision Guide

```text
用户要做什么？
├─ 展示个人经历、作品和联系方式 → 轻量静态网站，读 personal-site.md
├─ 已有网站继续完善或上线 → 保留架构，定位最早未验证阶段
├─ 真正需要账号、共享数据或后台 → 读 architecture.md 和 data-ai.md
└─ 需要支付、实时协作或重计算 → 选专用能力，按实际业务验收
```

推荐静态路线是减少不必要的开发与维护；不是限制用户指定的框架。具体版本、托管平台、价格与CLI参数均按当前官方文档核验。

## Workflow

### 1. Turn materials into a public brief

读取 [个人网站方法](references/personal-site.md)。用 [内容模板](assets/portfolio-content.md) 整理目标读者、个人介绍、代表作品及联系入口。列明允许公开、需要遮盖和不公开的内容；不编造经历、成绩、客户、获奖、评价或项目效果。

### 2. Build one complete personal site

选最小足够架构，读取 [开发方法](references/build.md) 和 [设计验收](references/design.md)。在空目录初始化；已有项目增量实现。用真实材料完成一条“认识我 → 看作品 → 了解贡献 → 联系我”的旅程，再完善其他内容。

### 3. Validate and show a preview

检查手机与桌面、导航、作品链接、键盘操作、联系方式、深链/404、生产构建及适用代码检查。生成可审阅的预览；没有预览发布授权时先给本地可运行成果。将模拟、跳过和真实验收分开记录。

### 4. Connect a domain and publish

读取 [域名与HTTPS](references/domains.md) 和 [部署与回滚](references/release.md)。先使用托管平台提供的地址验证，再按用户目标连接自有域名；需要购买时展示准确域名、归属账号、总价、续费、年限和自动续费方案。沿用已有授权，付款和生产操作不扩大到未授权范围。

### 5. Deliver a site the user can explain

在正式URL验收后，交付运行方法、资源归属、版本、修改入口、续费与恢复步骤。填写 [AI辅助制作记录](assets/build-notes.md)，帮助用户讲清真实需求、AI的作用、自己做出的判断、实际验证和后续改进。

没有模型能力的网站可表述为“使用AI辅助制作并上线的个人网站”；不能包装成已实现AI产品功能。无需为了面试强行添加模型API或生成虚假作品。

## Quality Rules

- 保留用户已批准的公开边界。简历中的手机号、学校、地址、客户材料等不会因为输入给代理就自动获准发布。
- 一次完成一个可操作的切片；不以模板页面数、依赖数或测试数替代作品价值。
- 有私有数据时校验身份与对象权限；浏览器存储、进程内存和云端持久化如实区分。
- 使用当前官方资料，不照抄旧价格、DNS值、部署账号或工作流ID。
- 声称正式上线前验证生产URL、HTTPS和关键动作；HTTP 200、截图或本地构建各自有证据边界。
- 只在获准协作时委派，并分配文件所有权；自审不称为独立审查。
- 外部调用重复失败2–3次后换诊断方法；缺少账号/授权时完成其他工作并交付具体待办。
- 不保证固定耗时或全网最快。以减少无用功能、尽早预览和打通真实任务来缩短交付路径。

## Reference Map

只加载当前步骤需要的文件。

| 任务 | 参考 |
|---|---|
| 个人内容、作品组织、公开边界 | [personal-site.md](references/personal-site.md) |
| 架构选择、其他网站类型 | [architecture.md](references/architecture.md) |
| 环境、契约、开发切片 | [build.md](references/build.md) |
| 页面、响应式与可访问性 | [design.md](references/design.md) |
| 账号、数据、AI、邮件与支付 | [data-ai.md](references/data-ai.md) |
| 域名选购、DNS与证书 | [domains.md](references/domains.md) |
| CI、平台部署、验收与回滚 | [release.md](references/release.md) |
| 可选技能与替代方法 | [skill-routing.md](references/skill-routing.md) |
| 当前官方文档入口 | [sources.md](references/sources.md) |

## Completion Criteria

按实际进度报告“本地可运行 / 预览通过 / 已部署待验收 / 正式验收完成”。给出站点入口、当前版本、验证证据、维护方法与未完成项。用户要实际建站时，持续完成获准的实现与上线工作，不以交付计划文档代替网站。
