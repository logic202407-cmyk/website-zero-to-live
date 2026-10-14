# 安全与隐私问题

本项目分发建站方法、模板和校验脚本。安全报告可以涉及指令导致的越权操作、公开个人材料、凭据泄露、危险部署建议及打包工具问题。

## 如何报告

- 若仓库 [Security 页面](https://github.com/logic202407-cmyk/website-zero-to-live/security)提供 **Report a vulnerability**，优先使用该私密入口。
- 若未提供私密入口，可在[仓库 Issues](https://github.com/logic202407-cmyk/website-zero-to-live/issues)仅请求建立私密联络渠道，不附漏洞利用步骤、私人材料或凭据。维护者确认私密渠道后再提供详情。
- 不要在公开 Issue、Pull Request、评论、日志或截图中发送密码、API key、访问令牌、完整简历或他人的个人信息。

报告中尽量包含受影响版本、相关文件/步骤、影响范围、脱敏后的最小复现和建议修复。不要为证明问题而访问他人的数据或操作未授权资源。

若发现凭据已经公开，应先由获授权人员在原服务撤销或轮换，再评估并处理仓库历史、构建产物、缓存及下载副本；删除当前文件不能消除历史副本。不要只隐藏页面链接或添加 `robots.txt`/`noindex` 后继续使用原凭据。参见 [GitHub 敏感数据处理说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)。

## 处理范围

修复优先进入最新版本；当前不承诺旧版本长期维护、固定响应时间或漏洞奖励。第三方宿主、安装器和托管服务的问题应同时通过其官方渠道报告。

使用者仍需按具体项目检查依赖、数据权限、域名与部署配置。模板不会授予代理额外账号、付款或发布权限。

个人展示站不应用于存储重要或敏感资料。完整简历、身份证件、财务或健康资料、客户保密文件及他人未授权信息应留在合适的受控系统中；详细边界见 [LEGAL.md](LEGAL.md)。
