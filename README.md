# Personal Website Launch

用 AI 把你的经历、作品和求职方向整理成一个属于自己的个人网站，并推进到公开访问和自有域名上线。

这是一个面向求职者的 **Agent Skill**。你提供材料和目标，代理负责组织内容、设计页面、实现、验证并准备部署。设计、运营、产品、市场、写作与技术岗位都可以使用。

默认交付轻量个人网站：个人介绍、代表作品、本人贡献、求职方向与联系入口。登录、数据库、支付或模型功能在确有需要时再增加。

**Skill name:** `website-zero-to-live` · **Version:** `1.1.2` · **License:** [MIT](LICENSE)

**安全提醒：不要把重要或敏感资料存储在个人网站中。** 个人展示站不是敏感资料保险箱。不要把密码、密钥/token、身份证件、财务或健康隐私、客户保密文件及他人未授权资料放进网站、前端资源、公开仓库或构建产物。只发布明确允许公开的最少内容；隐藏链接、`robots.txt` 和 `noindex` 不能代替访问控制。

使用前请阅读[法律声明](LEGAL.md)与[安全说明](SECURITY.md)，了解资料与历史副本的泄露风险、AI 输出、第三方托管、费用、素材权利和责任边界。

## Installation

### Requirements

- 能读取 `SKILL.md` 的代理宿主。实际建站需要相应文件、终端、预览/浏览器工具，部署需要目标账号和明确授权。
- CLI 安装需 Node.js/npm（提供 `npx`）；手动复制不需要 Node.js。
- 本项目是方法和模板包，不是已经生成的网站。框架和托管平台按具体项目选择，安装技能不会自动购买域名、上传材料或获得账号权限。
- 仅维护者构建与校验分发包需要 Python 3.10+；脚本只使用标准库。

### Using the skills CLI

在希望使用技能的项目目录运行：

```sh
npx skills add https://github.com/logic202407-cmyk/website-zero-to-live --skill website-zero-to-live
```

或者下载/克隆仓库，在含有 `SKILL.md` 的根目录运行：

```sh
npx skills add . --skill website-zero-to-live
```

安装器会提示选择代理和安装位置。仅查看技能、不安装：

```sh
npx skills add . --list
```

### Manual installation

取得仓库 `dist/website-zero-to-live-1.1.2.zip` 与相邻的 `.zip.sha256`，或使用维护者发布的同版本附件。解压后，将完整 `website-zero-to-live/` 文件夹复制到目标代理实际公布的技能目录，保留 `LICENSE` 及所有随包文件，然后刷新技能发现或开启新会话。安装包也包含本 README、使用说明和贡献文档。

也可以直接要求代理读取仓库中 `SKILL.md` 的本地绝对路径。不同宿主的自动发现与工具支持以其当前说明为准。

校验下载文件：在 ZIP 和 `.zip.sha256` 所在目录运行 Linux 的 `sha256sum -c website-zero-to-live-1.1.2.zip.sha256`，或 macOS 的 `shasum -a 256 -c website-zero-to-live-1.1.2.zip.sha256`。校验值与文件应来自可信的同一版本；哈希用于发现损坏或内容差异，不等于发布者数字签名。

## Quick Start

```text
使用 $website-zero-to-live，帮我做一个用于秋招的个人网站并推进上线。
目标岗位：产品/运营。
我会提供简历和两个代表案例，请突出真实贡献、过程和成果。
先使用托管平台地址给我预览，再提供域名购买和上线方案。
联系方式只公开邮箱，其他私人信息不要放上网站。
预算：……；本轮允许的开发与发布范围：……
```

更多示例见 [USAGE.md](docs/USAGE.md)。没有完整简历也可以先从一段自我介绍和一份真实作品开始；资料不足时标明缺项，不生成虚假经历填充页面。

## What You Get

- 围绕目标岗位组织的个人介绍和作品页面。
- 可运行的源码，以及手机/桌面检查与预览。
- 域名选购、DNS、HTTPS和部署流程；实际执行取决于账号、预算与授权。
- 后续修改、续费、回滚和维护方法。
- [AI辅助制作记录](assets/build-notes.md)：帮助你在面试中讲清楚制作过程和自己的判断。

使用AI辅助完成的网站，与网站本身具有AI功能，是两种不同成果。这里帮助你做出并理解真实作品，不保证面试结果、固定交付时间或全网最快。

## How It Works

```text
公开材料与目标
    → 轻量个人网站
    → 手机/桌面验证与预览
    → 正式网址、域名与HTTPS
    → 面试制作记录与维护交接
```

高级业务站、账号系统、支付或AI工具仍可使用通用架构和部署参考。

## Structure

```text
website-zero-to-live/
├── SKILL.md           # 触发场景、决策与主流程
├── LICENSE            # MIT 许可证
├── CONTRIBUTING.md    # 贡献与本地验证
├── SECURITY.md        # 安全报告和隐私提醒
├── THIRD_PARTY_NOTICES.md # 第三方来源与素材范围
├── CHANGELOG.md       # 版本变化
├── LEGAL.md           # 法律声明与使用边界
├── agents/            # 可选的代理UI元信息
├── references/        # 按需加载的详细方法
├── assets/            # 内容、制作和交付模板
├── docs/              # 使用、验证与实践说明
├── scripts/           # 可重复构建和完整性验证
├── tests/             # 发布工具回归测试
├── dist/              # 可直接分享的技能包
└── SHA256SUMS         # 分发文件校验
```

核心入口：[SKILL.md](SKILL.md)。个人网站路线：[personal-site.md](references/personal-site.md)。域名步骤：[domains.md](references/domains.md)。部署与恢复：[release.md](references/release.md)。

## Format References

入口、分层参考和README结构参考了公开技能的组织方式：

- [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)：简明的任务入口和可执行指导。
- [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md)：适用场景、快速索引和细分参考。
- [OpenAI Cloudflare Deploy](https://github.com/openai/skills/blob/main/skills/.curated/cloudflare-deploy/SKILL.md)：前置条件、决策分支和按需参考。
- [Cloudflare Skills](https://github.com/cloudflare/skills)：独立技能和多代理安装说明。
- [Vercel skills CLI](https://github.com/vercel-labs/skills)：技能发现与安装命令。

本仓库未包含上述第三方技能正文或资产。

## Validation and Reuse

在仓库根目录可运行本地检查：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/release.py check
```

验证范围见 [VALIDATION.md](docs/VALIDATION.md)，重新构建与发布步骤见 [RELEASING.md](docs/RELEASING.md)。实际网站按其目标、运行环境及授权执行相应验收。

## Contributing and Security

问题与建议可在 [Issues](https://github.com/logic202407-cmyk/website-zero-to-live/issues) 提出，提交修改前请看[贡献指南](CONTRIBUTING.md)。涉及凭据、隐私或漏洞的内容先看[安全报告方式](SECURITY.md)，不要公开粘贴敏感资料。

## License

本仓库原创内容采用 [MIT](LICENSE)，允许在保留版权与许可通知等条件下使用、修改和分发，包括商业使用。使用风险见[法律声明](LEGAL.md)，第三方工具与素材遵守各自许可，参见[第三方说明](THIRD_PARTY_NOTICES.md)。
