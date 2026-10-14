# Personal Website Launch 1.1.2

版本：1.1.2。发布日期：2026-10-14。

本版本完善开源许可、安装体验、贡献入口和可复现分发，继续以个人主页、求职作品集和简历网站为默认场景。

## 主要更新

- MIT 许可证随源码和安装包分发，法律声明与许可范围保持一致。
- README 提供实际仓库安装命令、运行要求、目录结构、使用示例及完整性校验方法。
- 增加贡献、安全报告、第三方来源和维护者发布文档。
- 明确不要将重要或敏感资料存储在个人网站，补充公开范围、泄露风险和发布前安全检查。
- 分发内容统一放在 `website-zero-to-live/` 下，携带 `MANIFEST.json` 文件哈希清单。
- 提供只依赖 Python 标准库的构建、校验与回归测试，以及验证 CI 配置。

## 安装与升级

命令安装及手动安装步骤见 [README](../README.md)。从旧版升级前，保留自行修改的模板或参考文件，比较后再替换技能目录；网站项目本身无需迁移框架或重新生成。

旧版 ZIP 顶层的 `USAGE.md`、`VALIDATION.md` 和 `PRACTICES.md` 已归入技能目录内的 `docs/`；使用入口仍是 `website-zero-to-live/SKILL.md`。

## 发布附件

- `website-zero-to-live-1.1.2.zip`
- `website-zero-to-live-1.1.2.zip.sha256`
- `SHA256SUMS`

验证范围和复现命令见 [VALIDATION.md](VALIDATION.md)，完整改动见 [CHANGELOG.md](../CHANGELOG.md)。
