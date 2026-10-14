# 从选域名到HTTPS

域名注册商负责所有权/续费；权威DNS负责解析；托管平台负责运行网站；证书负责HTTPS。它们可以属于不同供应商。更改NS不会自动迁移邮箱，也不等于转移域名注册商。

## 1. 形成可购买方案

从品牌可读性、易拼写、业务匹配、受众习惯选择少量候选。在注册商实际查询可用性，记录时间；同名公司/商标的公开检索只能作风险筛查，不能称为法律清权。

比较首年含税价、常规续费、转入成本、是否premium、隐私保护、年限、自动续费和币种；缺少价格就写未知，不复用旧案例中的优惠价格。

付款前向用户展示：准确域名、注册商、归属账号、年限、最终总价、续费价格/未知项、自动续费设置、额外服务。明确授权已覆盖此笔购买时直接按授权执行；否则只为这笔实际交易请求批准，不在准备工作前先泛泛询问。

在用户/组织账号注册，用户完成登录/2FA及必要身份资料；不要让代理账号成为域名持有人。核验付款与域名控制台结果，勿因超时重复下单。记录到期日、恢复联系人、续费负责人及2FA恢复方式所在位置，不记录密码、卡号或恢复码。用户要求提醒时才创建提醒工具任务。

## 2. 准备DNS变更

若已有域名：先导出/记录当前权威NS、A/AAAA、CNAME、MX、TXT、CAA和DNSSEC/DS。询问或识别现有网站、邮箱及其他子域名用途；保留与本任务无关记录。

先取得托管平台为这个项目给出的准确记录或自定义域名绑定方式，形成“主机名／类型／旧值／新值／代理状态／TTL／用途”变更表。不要使用教程中的通用IP、别人的NS或旧平台目标。

## 3. 选择一种接入方式

**A. 保留现有DNS**：平台添加域名后，在当前权威DNS新增/修改所需A/AAAA/CNAME或验证TXT；根域名按DNS商支持的ALIAS/ANAME/flattening或平台要求处理。仅改实际需要的记录。

**B. 将权威DNS迁往Cloudflare**：添加zone→核对导入记录与邮箱→记录Cloudflare分配的准确NS→按注册商界面修改NS→验证zone Active与外部权威查询。DNSSEC需按供应商迁移步骤协调旧DS/签名与新DS，避免残留不匹配导致SERVFAIL；不要盲删不相关安全配置。

[Cloudflare完整接入说明](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/)与[Namecheap修改NS说明](https://www.namecheap.com/support/knowledgebase/article.aspx/767/10/how-to-change-dns-for-a-domain/)仅在选择相应供应商时使用。

Cloudflare Workers路线：为实际Worker添加根域名和需要的www等自定义域名，检查生成的DNS与证书；不要照搬Vercel的A记录到Workers。Custom Domain逐个匹配主机名，根域名配置不自动覆盖www。[官方Custom Domains说明](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)

Vercel路线：在项目域名设置拿到当前要求的记录，配置后等待验证；不要固化历史IP/CNAME。[官方域名配置](https://vercel.com/docs/domains/working-with-domains/add-a-domain)

## 4. 主域名、TLS与关联配置

选定canonical主域名。另一个主机名需有效解析、有效TLS且明确重定向或承载策略；HTTP转HTTPS，跨主机重定向保留路径/查询且无循环。API方法需要保持时选择适当重定向语义。

托管平台按其方案签发证书，检查签发状态、主机名、链及到期。自托管则配置ACME等自动续签并演练。使用代理时按源站方案设置TLS，避免Flexible与源站HTTPS重定向形成循环；不要关闭证书验证来通过测试。

HSTS在HTTPS和需要覆盖的子域均准备好后设置；不自动加入preload或includeSubDomains。同步生产认证Site URL/回调允许列表、Cookie域、CORS、邮件链接、支付回调和SEO canonical。

## 5. 验证与故障定位

只读命令示例，先替换域名：

```powershell
Resolve-DnsName example.com -Type NS
Resolve-DnsName example.com -Type A
Resolve-DnsName www.example.com -Type CNAME
curl.exe -I https://example.com
curl.exe -I https://www.example.com/a-real-route
```

Linux/macOS可用`dig`及`curl`。某些平台会flatten CNAME，不能因CNAME查询为空就判定故障。必要时查权威NS与第二个递归解析器，结合缓存TTL判断；查询结果不一致时先定位，不反复改记录。

依次排查：注册商NS→权威zone→目标记录→DNSSEC→绑定主机名→证书/CAA→HTTP重定向→应用路径。DNS正常后再查应用；不要等待一个固定时长后凭空宣称“传播完成”。

用未登录浏览器与目标受众网络验收根域名、www、深链刷新、404、静态资源和主动作。保留时间、实际URL、网络/设备与结果；单点200不能证明全球可达。

## 6. 域名维护

交接注册商与DNS/托管账号归属、NS/记录表、到期日、续费价来源、证书方案、邮箱、修改记录和回退值。域名回退受DNS缓存影响，不是即时回滚；上线窗口保留旧站和必要记录至验证完成。域名变更完成后再按新服务商官方流程启用/核验DNSSEC。
