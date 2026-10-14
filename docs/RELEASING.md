# 维护者发布流程

发布前完成下面的本地检查。提交、推送、创建标签和 GitHub Release 是单独的远程操作，只在仓库维护者决定发布后执行；本地生成 ZIP 不代表已经发布。

## 1. 确认内容与版本

- 检查拟发布 diff、来源及许可，确认没有凭据、私人材料或未获授权的第三方资产。
- 更新 `SKILL.md` 的 `metadata.version`、README 版本及下载链接、变更记录和该版本的发布说明。
- 保留标准 MIT `LICENSE`，不得用法律声明替代许可或增加与 MIT 冲突的再分发限制。
- 需要更换 `dist/` 中的版本时，仅移除已确认由新版本替换的旧 ZIP 和对应 `.sha256`。旧版本由 Git 历史及已发布 Release 保留，不能覆盖同一标签的已发布产物。

## 2. 构建与验证

要求 Python 3.10 或更新版本，无第三方 Python 依赖。在仓库根目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/release.py build
python3 scripts/release.py check
git diff --check
```

构建生成 `dist/website-zero-to-live-<version>.zip`、相邻 `.zip.sha256` 和根目录 `SHA256SUMS`。同一份源文件重复构建应得到相同字节；校验命令检查入口信息、文本与相对链接、敏感模式、包成员、许可、清单、源码一致性及哈希。

ZIP 解压后只有 `website-zero-to-live/` 一个根目录；其中 `MANIFEST.json` 记录技能名称、版本、MIT 许可及各文件 SHA-256。清单不记录自身哈希；ZIP 的外部校验值负责覆盖整个归档。SHA-256 用于完整性校验，不等于数字签名或发布者身份认证。

若要额外检查宿主发现，可使用已审核的 skills CLI：

```sh
npx skills add . --list
```

此命令仅列出技能。真实安装测试应在独立临时目录或测试账号中执行，记录 CLI/宿主版本，避免改动日常工作环境。

## 3. 检查发布候选

- 在独立临时目录解压新 ZIP，进入 `website-zero-to-live/`，先运行随包单元测试，再运行 `build` 和 `check` 重建并检查，确认许可证、文档和引用完整。原始 ZIP 的 `MANIFEST.json` 可用于逐文件复核；包内不包含嵌套 ZIP 或仓库级 `SHA256SUMS`。
- 更新验证记录中的实际日期、命令和结果；未执行的检查不写成通过。
- 审核最终 diff、ZIP 及校验值；内容再变更后重新运行构建和检查。
- 将变更记录的“待发布”改为实际发布日期，提交完整源码、ZIP 和校验文件，并在该精确提交上运行 CI。

## 4. 正式发布

获得维护者发布决定后，在已通过验证的精确提交上创建对应 `v<version>` 标签及 GitHub Release。发布正文使用该版本说明，例如 [1.1.2 发布说明](RELEASE_NOTES_1.1.2.md)，附上 ZIP、对应 `.sha256` 和 `SHA256SUMS`。

最后核对远端提交、标签、Release 附件与本地哈希一致，再宣布发布完成。不要把本地测试结果写成远端 CI 已通过。
