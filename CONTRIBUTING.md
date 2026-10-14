# 参与贡献

欢迎改进个人网站路线、安装说明、通用模板、参考资料及验证工具。提交前请阅读 [README](README.md)、[使用说明](docs/USAGE.md) 和 [MIT 许可证](LICENSE)。

## 报告问题

一般问题请使用[仓库 Issues](https://github.com/logic202407-cmyk/website-zero-to-live/issues)。说明技能版本、代理宿主及版本、操作系统、最小复现步骤、预期行为和实际结果。日志与截图先去除密钥、私人联系方式、账号信息和客户材料。

涉及漏洞、凭据或隐私泄露时，遵循 [SECURITY.md](SECURITY.md)，不要在公开 Issue 里提交敏感细节。

## 提交修改

1. Fork 仓库，从当前默认分支创建工作分支。
2. 一次聚焦一个问题。保留已有框架和用户公开边界；不要加入真实简历、私有案例、账号、部署凭据或机器绝对路径。
3. 修改方法时同步相关参考和示例。第三方内容保留来源及许可，新增依赖前说明必要性。
4. 更新 [CHANGELOG.md](CHANGELOG.md)。只有发布新版本时才更新 `SKILL.md` 的版本与 README 的包链接。
5. 在仓库根目录运行以下检查。Python 工具只使用标准库，不需要安装依赖：

   ```sh
   python3 -m unittest discover -s tests -v
   python3 scripts/release.py build
   python3 scripts/release.py check
   git diff --check
   ```

6. 提交 Pull Request，说明改动原因、验证命令和结果；有可见行为变化时附匿名化证据。没有执行的检查不要写成通过。

维护发布包时请阅读[发布流程](docs/RELEASING.md)。不要手工修改 ZIP 或哈希文件；文档或源码有变更后重新构建并验证。

## 贡献许可

提交贡献即表示你有权提供这些内容，并同意按本项目的 MIT 许可证分发你的贡献。第三方内容仍遵守其原有许可；不要提交无法确认来源或授权的材料。无需转让你对贡献拥有的权利。

交流请聚焦问题本身，尊重不同经验和背景。维护者按实际时间处理贡献，不承诺固定响应时限。
