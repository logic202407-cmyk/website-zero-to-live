# Website Zero to Live

一套将网站想法推进到可维护的正式上线的通用 Agent Skill。

覆盖需求、架构选择、设计开发、账号与数据、质量检查、域名选购、DNS/HTTPS、部署、公网验收、回滚及运维。按展示站、内容站、会员系统、商城、AI 工具等类型选择适当复杂度，不要求所有网站采用同一技术栈。

## 快速开始

仓库根目录的 [SKILL.md](SKILL.md) 是技能入口。首次使用可直接让代理读取该文件的本地绝对路径。

```text
使用 $website-zero-to-live，帮我从零构建并上线一个网站。
用途：……
目标用户与地区：……
核心功能：……
预算：……
已有代码、域名和账号：……
本轮允许执行的开发与发布范围：……
```

技能会先核对现有资源并完成可执行工作；缺少购买或发布授权时，先准备具体订单、验证证据和发布方案。不会自动支付、充值或把模拟结果当作正式验收。

## 获取与安装

下载 [1.0.1 分享包](dist/website-zero-to-live-1.0.1.zip)，将其中完整的 `website-zero-to-live/` 文件夹复制到目标代理实际公布的技能目录。

也可以下载或克隆本仓库，将根目录的 `SKILL.md`、`agents/`、`references/` 和 `assets/` 放入目标技能目录下的 `website-zero-to-live/` 文件夹。不要只复制入口，也不要多嵌套一层同名目录。公开仓库可直接访问和下载。

不同代理的发现目录与刷新方式可能不同，以目标环境的当前说明为准。安装后刷新技能发现或开启新会话，确认列表出现 `website-zero-to-live`；也可直接要求代理读取入口文件的实际绝对路径。

## 文件导航

| 内容 | 入口 |
|---|---|
| 技能主流程 | [SKILL.md](SKILL.md) |
| 架构和网站类型选择 | [architecture.md](references/architecture.md) |
| 开发方法 | [build.md](references/build.md) |
| 设计与交互验收 | [design.md](references/design.md) |
| 账号、数据与 AI | [data-ai.md](references/data-ai.md) |
| 域名购买、DNS 与 HTTPS | [domains.md](references/domains.md) |
| CI、部署、验收及回滚 | [release.md](references/release.md) |
| 可选技能组合与替代方法 | [skill-routing.md](references/skill-routing.md) |
| 官方资料入口 | [sources.md](references/sources.md) |
| 项目简报、开发和发布模板 | [assets](assets) |
| 可复用的网站交付经验 | [实践总结](docs/WEBSITE_DELIVERY_PRACTICES.md) |
| 使用示例 | [使用说明](docs/USAGE.md) |
| 验证范围 | [验证说明](docs/VALIDATION.md) |

## 适用范围

版本：1.0.1。方法与模板独立于特定业务项目；不包含业务源码、真实凭据、用户数据或第三方技能副本。其他 UI、数据库等技能均为可选增强，缺少时有内置方法。

元信息、引用与文件完整性检查不能证明任意网站均能上线。实际项目仍需真实账号、内容、必要预算与目标运行时验收。引用第三方项目不授予其代码、品牌或素材使用权。本仓库未指定开源许可证，不应把访问权限视为开源授权。

`SHA256SUMS` 用于核对本次分发文件；ZIP 内另有文件清单。修改内容后需重新生成对应清单。
