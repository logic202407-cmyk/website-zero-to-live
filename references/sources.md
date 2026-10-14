# 官方资料入口

本包整理于2026-10-13。入口用于再次核验，不能把整理日期当作未来可用性/价格保证。执行时优先已安装版本文档与对应官方发布说明；记录访问日期和适用版本。以下为本次检索使用的主要官方来源。

- [Next.js安装](https://nextjs.org/docs/app/getting-started/installation)：脚手架、运行时与启动。
- [Next.js自托管](https://nextjs.org/docs/app/guides/self-hosting)：生产进程、缓存、多实例与反向代理。
- [Cloudflare的Next.js入口](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/)：当前路线与兼容信息。不同适配路线的推荐状态与成熟度会变化，选择前核对当前官方说明，不自动迁移既有项目。
- [OpenNext Cloudflare](https://opennext.js.org/cloudflare)：OpenNext适配器的官方入口。
- [Cloudflare Workers Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)：主机名绑定、证书、根域名与www。
- [Cloudflare完整DNS接入](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/)：NS迁移与DNS检查。
- [Namecheap更改DNS](https://www.namecheap.com/support/knowledgebase/article.aspx/767/10/how-to-change-dns-for-a-domain/)：注册商NS设置实例；不提供即时价格。
- [Vercel配置域名](https://vercel.com/docs/domains/working-with-domains/add-a-domain)：读取项目实际要求的DNS记录。
- [Supabase更新日志](https://supabase.com/changelog)：先查相关breaking changes；本次`.md`入口读取失败，使用HTML入口。
- [Supabase SSR客户端](https://supabase.com/docs/guides/auth/server-side/creating-a-client?queryGroups=framework&framework=nextjs)：客户端/服务端会话实现。
- [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)：数据权限与策略。
- [Supabase API安全](https://supabase.com/docs/guides/api/securing-your-api)：Data API暴露、授权与RLS的不同职责。
- [GitHub手动运行工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)：工作流入口与触发方式。

这是经过筛选的入口，不是完整教程镜像。第三方内容保持链接与简短方法总结；具体套餐价格、DNS值、模型名、配额和供应商UI都在执行时重新读取。未能访问官方资料时记录缺口，继续不依赖该信息的本地工作，不编造可执行参数。
