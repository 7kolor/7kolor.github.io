# 7Kolor Insights — 2026 W46 周报

## 三条商业情报：谁在付钱、定价权在谁手里、流量换成了什么

> 本周最具体的付费信号来自噪音取证，出现捐赠与复刻意愿；定价权的雷点是什么会被收回；部分搜索流量明显下滑，AI 引用是新增渠道——本周商业情报。

原文 / Source: /weekly/2026-W46/

---

**本周主线一句话**：先看清谁在为什么付钱，再把定价权写进合同，最后把获客从「写更多内容」换成「被引用」。

> 「OP, throw up a donation link I will give you some money if you want.」

 [本周最具体的付费信号](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/19sumrvcqav9h/)——客户要的不是设备，是能提交给市政的投诉材料
- **本周最具体的付费信号**：1 · 社区噪音取证：受害者愿为「被证明」付钱
- **AI 按次付费中位月收入**：$0.29 · 1,536 个服务，未经第三方核验
- **想付费却买不到的起售档**：100 · OpenCloud 最低档按 100 用户起售
- **某搜索词的年跌幅**：56% · html2pdf——功能型 SaaS 的渠道正在消失

**怎么读这份报告**：只有 15 分钟就读第一、二节和第七节；你在找方向，第三、四节是钱与雷；你在做产品，第五节新品雷达值得扫一眼。

  本期速览  本周最硬的三条 [**最具体的付费信号来自取证**出现捐赠与复刻意愿，持续付费仍待验证](#top3) [**定价权的雷点不是价格**是「什么会被收回」；想付费的人买不到 100 用户起售档](#top3) [**部分搜索流量下滑，AI 引用是新增渠道**替代路径是被引用，但成交归因仍待验证](#top3)  我们替你否掉的 [**给 AI 卖调用次数**1,536 个样本，中位卖家月收入 29 美分](#reject) [**把 AI 引用监测当成空白**监测与助手流量统计已有实现，成交归因待验证](#reject)  还在等证据的 [**AI 答案 → 客户的归因**监测与助手流量统计已有实现，成交归因待验证](#top3) [**功能型 SaaS 会不会被白送**本期只有渠道侧的证据：html2pdf 搜索量 -56%](#signals)

## 一、本周三件最重要的事

 本周最具体的付费信号来自噪音取证；定价权的雷点不是价格而是「什么会被收回」；部分搜索流量明显下滑。      01

### 本周最具体的付费意愿来自噪音取证，捐赠与复刻意愿同时出现

[社区噪音自动取证](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/)：用 30 美元清仓平板采集噪音、准备向市政汇报的楼主，评论区同时出现了愿付钱、想复制和要买同款硬件三种人。

**客户要的不是设备，是能提交给市政的投诉材料**

> 「OP, throw up a donation link I will give you some money if you want.」，u/Hasz，42 分；

> 「i would be very interested in mimicking this project.」，u/dope_zebra，52 分。

所以先验证用户是否会为可提交的投诉材料持续付费，再做采集端、本地分类与一键导出。

**反面样本同周出现：1,536 个「AI 按次付费」服务**总量约 $40,000，top 7 拿走约 $30.5k，其余 1,529 个分摊约 $9.8k，中位卖家收入 29 美分，1,034 个整月不到 $1，约 1/3 根本不交付。错在单位价值低于单位成本，不在「按次付费」这个模式；同周的正面样本把按次付费用在单价高、有真实结果的动作上——$3/篇、能进榜单的文章。

**动作**给你的产品写一句「客户为什么付钱」，答案里必须出现一个可交付的结果，而不是一个功能；把最小可计费单位的价格抬到能覆盖一次交付的倍数；如果你正考虑做 AI 自动付费的小服务，先算中位数而不是均值。

  02

### 客户为「所有权」付钱，为「会被收回」离开——三件事指向同一个位置

[Infisical 在 patch 版本里把 custom roles 变成企业版专属](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/)：被锁住的偏偏是「限制机器身份能做什么」这一项——在 secrets manager 上等于零权限管理。

**信任是分三阶塌掉的**第一步，patch 版本做破坏性变更；第二步，文档先悄悄改而发布说明不写；第三步，想付费的用户找不到销售——

> 「The sales person said it wasn't possible… then they stopped responding. It is not a serious company.」，u/_f0CUS_，95 分。

社区的反应不是「贵」，是「你不懂我为什么在这里」。

**想付费的人买不到档**OpenCloud 把生产版锁进订阅本身没翻车，翻车的是档位：

> 「Im interested in the Basic subscription also to support the project but on the pricing page it says starting from 100 users.」，u/siegfriedthenomad，8 分。想付费支持的小团队买不到一档。

**上游涨价传导下来的是迁移，不是付费**[Last.fm API 绑定 Pro](https://www.reddit.com/r/selfhosted/comments/1xzka97/lastfm_api_keys_will_require_pro_from_1st_december/)：

> 「$4.99 a month. GTFO. I'll just subscribe to Spotify again」，u/SolFlorus，214 分。当产品可以被一个周末重写出来，价格就失去了地板：

[「a cloned app has no floor at all」——u/drakatmm](https://www.reddit.com/r/micro_saas/comments/1xzgs3p/saas_as_we_know_it_is_dying_and_wispr_flow_is_the/19sv8nc2oveud/)

 本周同一批帖子里的价格刻度：卖方收入与成本 vs 客户付费与平台抽成

图中刻度：卖方侧 $0.29、$29、$215 → $4、$2–3/月；客户与平台侧 $4.99/月、约 30%、$100/月、100 用户起售。

**动作**把「你永久拥有什么、什么会被收回」写进定价页和合同；给自己的产品留一个 1–20 人的小团队档，别让最小档从 100 用户起售；列出你依赖的每个第三方 API 的「涨价/封禁那天我的替代路径」，没有替代路径的就是单点风险。

  03

### 部分搜索流量明显下滑，AI 引用是新增渠道

[搜索流量 -40% 帖](https://news.ycombinator.com/item?id=50540178)——原帖作者就是 slashdev，40% 来自第三方统计口径，不是社区共识。但评论区实测更差：「My traffic is down over 80%. … By December next year I'll probably have to put the website in maintenance mode and find another job.」，u/nicbou。

**反驳必须在场：需求没消失，渠道在换**搜索量下降不等于需求下降——

> 「our sign up rate and conversions are significantly higher. AI feeds in better leads than just a single search query.」，u/robeym；还有冷客户直接来自 ChatGPT 的案例，u/komali2。

同时别丢掉还没失效的引擎：本期一位独立开发者的 15,000 注册里，八到九成来自 SEO 与 AEO，转化约 3%。

**AI 引用是新增渠道，归因能力仍待验证**最直接的需求信号来自一位独立开发者公开问「How to gain visibility in AI tools like chatGPT?」，72 条评论在给答案：

> 「One mention in a well-trafficked listicle beats ten posts on your own blog.」，u/cethu3001，6 分。但要诚实：可见度监测已经有产品，助手流量统计也有人开源实现。「哪条答案带来注册或收入」仍是待验证的问题，不是已证空白——

> 「no public dashboard shows who references your brand in their answers」，u/brilliantzen，1 分，同帖。该评论同时推广自己的相关工具，只作需求线索，不作市场证据。

**动作**今天做四件事：认领域名、查 robots.txt 与 Cloudflare 是否默认拦了 AI 爬虫、把定位与定价写成纯文本、主动查自己是否被引用。把内容预算从「写更多」换成「进第三方榜单与评测页」；如果你的流量主要来自搜索，先做一次归因体检再决定要不要改内容策略。

## 二、痛点：五个能落到经营上的

 五个痛点全部落在钱上：渠道、定价权、档位设计、单点依赖、单位经济。每条给出机制、今天能做的动作与适用对象。

#### 1. 分发：流量结构在换，AI 归因能力待验证

 −80%个人实测流量下滑370/400首页访问里是爬虫−56%html2pdf 搜索量年跌

[怎么在 AI 工具里获得曝光](https://www.reddit.com/r/Entrepreneur/comments/1xyitwp/how_to_gain_visibility_in_ai_tools_like_chatgpt/)：AI answers 拿走「看答案」的流量，索引变慢、爬虫稀释，部分依赖搜索的内容站流量明显下滑，变现能力需要单独核验。AI 引用是新增渠道；哪条答案带来客户，仍待验证。

 翻面看可抄动作 →

##### 可抄动作

四件事：认领域名、查爬虫拦截、写纯文本定位页、主动查是否被引用。把内容预算从「写更多」换成「进第三方榜单与评测页」。

适用：靠搜索与内容获客的人

出处：[原帖](https://www.reddit.com/r/Entrepreneur/comments/1xyitwp/how_to_gain_visibility_in_ai_tools_like_chatgpt/)

#### 2. 定价权不在你手里：上游涨价传导的是迁移

 $4.99上游 API 月费160「又一个披着开源外衣的脏公司」13已经迁移走人的评论

[Infisical patch 版偷付费墙](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/)：上游涨价的传导通常不是涨价，而是逼你换路径或关停。patch 版本偷付费墙损失的不是那个功能，是社区的 star、PR 和答疑——那本来就是早期增长的来源。

 翻面看可抄动作 →

##### 可抄动作

列出每个第三方 API 的「涨价/封禁那天我的替代路径」，没有替代路径的就是单点风险；自己的产品，免费层不许锁死迁移路径，付费墙不要落在用户最在意的那一项上。

适用：用别人 API 的人，以及卖东西给人的人

出处：[原帖](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/)

#### 3. 信任被单方面破坏：想付费的人买不到档

 100OpenCloud 最低档起售用户数95「想付钱但买不到」的评论分13已经迁去 OpenBao 的评论

[OpenCloud 把生产版锁进订阅](https://www.reddit.com/r/selfhosted/comments/1xzj6gq/opencloud_the_nextcloudowncloud_alternative/)：订阅化本身没翻车，翻车的是档位：最低档按 100 用户起售，想付费支持的小团队买不到一档。破坏性变更提前公告、免费层不锁迁移路径，这些才是档位设计的底线。

 翻面看可抄动作 →

##### 可抄动作

给自己的产品留 1–20 人档；破坏性变更提前公告；先给迁移脚本再谈订阅。

适用：卖软件给开发者与小团队的人

出处：[原帖](https://www.reddit.com/r/selfhosted/comments/1xzj6gq/opencloud_the_nextcloudowncloud_alternative/)

#### 4. 单平台依赖：一次封禁归零，申诉是用一次即关闭的黑箱

 3,000+八个月攒到的订阅$0.76另一案例的可用余额~30%渠道佣金加支付手续费

[Substack 封禁归零](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/)：失败不是概率问题而是后果问题：你的资产全在别人的规则系统里，申诉还是用一次即关闭的黑箱。渠道本身也会成为成本项——佣金加支付手续费约三成，另有订阅费。

 翻面看可抄动作 →

##### 可抄动作

三份备份：名单、内容、支付渠道；再准备一个第二分发渠道；把「平台封禁我怎么办」写进应急预案第一页；入伙任何渠道前先算保本 GMV。

适用：只在一个平台获客的人

出处：[原帖](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/)

#### 5. 单位经济与规模上限：流量与收入脱钩最早报警

 $0.291,536 个按次付费服务的中位月收入$19.56clipr.cc 四年总收入$0.76LinkGenius 的可用余额

[LinkGenius 的 Stripe 面板](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/)：流量与收入脱钩、固定成本先见顶，这两个信号比任何增长指标都早。小生意最容易被低估的三项成本是时间、拒付与跨境固定费。

 翻面看可抄动作 →

##### 可抄动作

跑道月数 = 可用余额 ÷ 月 burn；看收益中位数而不是均值；固定成本占潜在收入超过 100% 就重定价；拒付防线三件事：改账单描述符、小额先退款不计为争议、跨境付款批处理。

适用：所有小生意

出处：[原帖](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/)

## 三、钱与人：付费信号与翻车样本

 这里不宣称成交：把付费意愿、定价与成本样本、以及翻车案例分开看。共同前兆是单位经济与迁移成本。 W1

#### [用 30 美元平板采集噪音](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/)

「OP, throw up a donation link I will give you some money if you want.」——u/Hasz

 **需求与样本价值**评论区同时出现捐赠、复刻与采购硬件的意愿；这证明兴趣，不证明持续付费。 **卡点**麦克风自动增益让分贝不可信，廉价硬件不可持续，证据可采性未验证。 **可抄条件**先验证租户、房主与业委会是否会为可提交的投诉材料付费；设备只是采集手段，形态可以是采集端 → 本地分类 → 一键生成投诉材料。  W2

#### [RankSpot](https://www.producthunt.com/posts/rankspot-2)

明码标价 $3/篇、$0.004/次 prompt 检查——厂商口径

 **需求与样本价值**按次付费用在单价高、有真实排名的动作上，而不是查天气这种免费替代品遍地的事。 **对照**同期 1,536 个同类服务，中位卖家月收入 29 美分。 **可抄条件**你的每次调用都能带来可计量的结果，而不是多一次 API 转手。  W3

#### [Codemany](https://www.producthunt.com/posts/codemany-2)

10 月 $215 → 11 月至今 $4——厂商口径

 **需求与样本价值**隐形开支被摊到台面本身就是产品价值：开发者第一次看见 CI 占掉多少。 **注意**只有这一个样本，runner 数、分钟数与规格都没公开，不能照抄成预算。 **可抄条件**你的产品存在一笔用户看不见、算得清的成本。  W4

#### [1,536 个服务的收入分布](https://www.reddit.com/r/passive_income/comments/1xwqicl/i_looked_at_what_1536_tiny_ai_pays_per_use/)

top 7 拿走约 $30.5k，其余 1,529 个分摊约 $9.8k，中位卖家 29 美分——楼主正文（第三方统计，未经核验）

 **需求与样本价值**当一个赛道的收入分布是稀缺信息时，公开分布数据让读者能判断是否值得进入；它是公开证据，不是收入证明。 **用法**先看总量，再看中位数，再看头部集中度，最后看交付失败率。 **可抄条件**你能持续、公开、可核地统计一个大家都在参与但没人统计的市场。  失败样本的规模对照（对数刻度；金额为当事人自述或楼主统计） L1

#### clipr.cc：四年 1,000 万次访问，总收入 $19.56

流量与收入彻底脱钩：日均 1.5 万次跳转、日活约 150 人，付费转化常年为 0。前兆不是流量不足，是固定成本早已吃掉潜在收入。

出处：[原帖与账本](https://www.reddit.com/r/SideProject/comments/1xx5n46/never_build_a_url_shortener_never/)

 L2

#### LinkGenius：八个月，MRR $29，可用余额 $0.76

月 burn $130–170。可用余额 ÷ 月 burn = 跑道月数；免费层与付费层功能没有差异，等于定价时消灭了付费理由。

出处：[Stripe 面板自述](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/)

 L3

#### Substack：八个月 3,000+ 订阅，一次封禁归零

评论区第一句问的是有没有定期备份帖子与订阅者名单。申诉没有 case ID、分钟级驳回，说明材料补得再细也未必有第二条通道。

出处：[封禁与申诉自述](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/)

 L4

#### 1stDibs：渠道成本把卖家的毛利吃光

佣金加支付手续费约三成，另有月订阅与广告位。入伙前先算保本 GMV，而不是先看平台流量。

出处：[卖家退出自述](https://www.reddit.com/r/Flipping/comments/1xx51w2/1stdibs_a_marketplace_that_has_lost_its/)

 L5

#### 冷启动：50 封精准冷邮件，零回复

评论区把样本量说清楚了：「Fifty emails is a sample size of basically zero」。先定样本量，再判断渠道；文案写业务结果，不写品类词。

出处：[冷启动失败自述](https://www.reddit.com/r/automation/comments/1xznabq/is_ai_automation_dead_has_every_business_in_the/)

 L6

#### AI 生成站点：交付收入变成维护负债

交付时省下的构建时间，换成插件兼容、测试与升级负债。没有测试套件的自定义代码，维护责任只能回到交付方。

出处：[建站维护讨论](https://www.reddit.com/r/Wordpress/comments/1xzehba/wordpress_will_be_fine_what_happens_to_builders/)

 clipr.cc 四年 1,000 万次访问、总收入 $19.56；LinkGenius 八个月 MRR $29、余额 $0.76；Substack 八个月 3,000+ 订阅、一次封禁归零；1stDibs 卖家被约三成渠道成本劝退；冷启动 50 封精准邮件零回复；AI 生成站点交付后变成维护负债。

## 四、我们替你否掉的方向

 否掉的不是需求，是被高估的读法：每一个都附了「什么情况下它仍然成立」。

### 给 AI 卖调用次数：1,536 个样本给出的分布，不是一个机会

[那份收入分布](https://www.reddit.com/r/passive_income/comments/1xwqicl/i_looked_at_what_1536_tiny_ai_pays_per_use/)：作者统计了 2026 年 10 月这类小服务的真实收入分布。

**机制：**按次付费把「需求」假设在前——它假定存在一个愿意自动按次付费的 AI 代理市场。本周的数据是：需求还没起来，供给已经挤了 1,536 个。

**反方也在场：**按次付费本身没问题：同周的正面样本把按次付费用在单价高、有真实结果的动作上，比如 $3/篇、能进榜单的文章。

**动作：**别做目录型生意；先算你的每次调用值多少钱、交付成本是多少。

 1,536 个按次付费服务的收入分桶（对数刻度；目录运营方自算，未经核验）

分桶数据：低于 $1 共 1,034 个；$1–10 共 360 个；$10–100 共 113 个；高于 $100 共 29 个。

### AI 代码质量「打分」：本周最被高估的机会

[审查瓶颈研究帖](https://news.ycombinator.com/item?id=50538303)：评论区一边要可量化的质量指标，一边质疑这种指标是否可定义。

**机制：**全帖最高分的评论都在要可量化的质量指标，但质疑同样明确：「Untested code is broken code」，没有定义好的架构与规范时 agent 只是在猜，还有人质疑原始数据对独立开发者的代表性。

**反方也在场：**能做的不是打分，是评审记录回灌、团队规范资产与漏检率跟踪。

**动作：**这一项证据不足，暂不立项，下周补证。

## 五、新品雷达

 开发者工具与 Agent 基建仍然最密，但热点已经从计费层移到了测试、验收、记忆与身份层；这一层当供应商用，别当竞品做。 当周发布动态的品类归属示意（不显示数量，不引用票数、评分与排名）

| 产品 | 做什么 | 为什么值得看 |
|---|---|---|
| [Tabstack by Mozilla](https://www.producthunt.com/posts/tabstack-by-mozilla-2) | 抓取与浏览器自动化做成托管 API，浏览器跑在你的模型之外，官方强调不用于训练、默认私密 | 当周唯一有大厂背书的隐私优先抓取层 |
| [Puffin](https://www.producthunt.com/posts/puffin-2) | 每个 AI agent 一个独立邮箱、聊天席位与日历 | agent 身份层成了独立品类 |
| [StateWeave](https://www.producthunt.com/posts/stateweave-2) | agent 在各应用的有状态克隆里跑，可注入宕机与 401 | 把「失败环境」做成基础设施，正对第一节的验证缺口 |
| [Codemany](https://www.producthunt.com/posts/codemany-2) | 自有基础设施跑 GitHub Actions，公开自己的账单 | 把 CI 成本摆到台面；仅一个样本，缺基线 |
| [Privacyboard](https://www.producthunt.com/posts/privacyboard) | 检出第三方工具并起草隐私政策、Cookie 横幅与 DPA | 合规是「有人替你踩过雷」的市场 |
| [RankSpot](https://www.producthunt.com/posts/rankspot-2) | 按量付费的 SEO 与 AI 搜索执行层，$3/篇 | 1,536 个失败样本的正确用法：按次付费用在单价高、有真实排名的动作上 |
| [AI Context Flow MCP](https://www.producthunt.com/posts/ai-context-flow-mcp) | 一份共享记忆经 MCP 覆盖多个 agent 与团队 | 跨工具记忆碎片化已被当成独立品类 |
| [Glassmail](https://www.producthunt.com/posts/glassmail) | Mac 邮件客户端，AI 完全本地跑，无订阅，一次买断 | 本地 AI + 一次性买断，与本周社区对被收付费墙的反弹同源 |

## 六、值得记下的信号

 按「对生意的影响」分档 直接影响收入

[功能型 SaaS 正在被商品化，渠道先承压](https://www.reddit.com/r/SaaS/comments/1xyg2q6/my_saas_makes_25kmonth_but_im_not_sure_it_has_a/)月入 €2,500 的 PDF API，老客没流失、新客持续下滑；评论区用数据指认渠道——「Search for "html2pdf" is down 56% YoY … Devs ask Claude instead of Google now.」，u/zggb，24 分。

[「高薪零工」铺帖获客是一门 referral 分销生意](https://www.reddit.com/r/RemoteWorkers/comments/1xxf2tt/get_paid_45hour_to_help_train_ai_no_programming/)同一账号两条帖、同一个 referral 码，评论合计五百余条全是应聘话术，没有一条讨论岗位内容——读者以为你在卖岗位，实际你在赚介绍费。

 改变定价与合同

[买断 vs 使用权是定价陷阱的核心](https://www.reddit.com/r/business/comments/1xzg87e/tesla_will_sell_you_a_cybercab_for_30000_then/)用户愤怒的不是贵，是「我买了它却不能靠它赚钱」——u/consultinglove，111 分。

[免费模型 API 不能对付费用户开](https://www.reddit.com/r/SaaS/comments/1y08vva/i_made_17k_usd_from_my_saas_and_here_are_the/)428 家第三方 API 路由器的研究里，9 家在响应中注入恶意代码、17 家碰过凭据——这是信任线，不是省钱线。

[托管成本的地板在每月两三美元](https://www.reddit.com/r/selfhosted/comments/1xy63oj/a_23mo_vps_is_the_best_remote_access_solution/)一台 $36/年的机器就是自托管方案的成本地板——这让「自托管/本地/一次买断」在成本上第一次成立。

 选品参考

[自托管的留存开关是一个具体设备](https://www.reddit.com/r/selfhosted/comments/1y1epug/be_honest_whats_the_selfhosted_service_you_spent/)「Getting an epson scanner to drop to the watch folder over SMB was what made me use it all the time.」——选品是硬件 + 一键配置 + 本地检索，不是软件本身。

[注册量是虚荣指标](https://www.reddit.com/r/SaaS/comments/1xz6qzx/i_just_crossed_15000_signups_in_my_saas_today/)15,000 注册、转化约 3%；评论区共识是漏斗漏在注册后的头几天——「teams obsess over top of funnel while the real leak is that first 5 minutes after signup and the first week after.」

## 七、上周说过什么，本周是否还成立

| 上周 W45 说过 | 本周证据 | 结论 |
|---|---|---|
| 接单要先设上限 | 反向案例：AI 自动升级失败率只有人类一半，但速度快 10 倍，每月事故数变 5 倍，u/tflinton | 维持；交付前把验证写进交付物 |
| 报价要认买方留出的区间 | Last.fm 把 API 绑 Pro，每月 $4.99，直接逼迁下游用户；Infisical 的付费墙挑中了用户最不能没有的那一项 | 维持，并补一层——上游涨价要提前准备替代与迁移路径 |
| 别为情绪付费 | 本周有多处付费意愿：噪音取证出现捐赠意愿，Infisical 出现销售失联，OpenCloud 出现档位缺口；它们都不是已成交证据 | 维持 |
| Agent 计费/用量层当供应商别做竞品 | 当周发布里计费与用量类已明显变少，热点移到开发者工具与 Agent 基建；Codemany 把 CI 账单摊开 | 维持，但位置从计费层挪到测试/验收/发布环层 |
 上期我们把 AI 的代码问题写成「代码变脆」，本周改口：脆是表象，排队才是机制——产出成本下降之后，真正的成本转移到了验收带宽上，而验收带宽不会自己变宽。上期否掉「AI 零工平台」时说的是供给过剩，本周更精确：供给过剩只是表象，单位价值小于单位成本才是机制。

## 八、本周行动清单

 2H

### 如果你只有 2 小时

- **1. 查一次 AI 爬虫拦截**：确认 robots.txt 与 Cloudflare 没有默认拦掉 AI 爬虫；把定位与定价写成纯文本页；认领 ChatGPT 里的商家资料，免费且只需 DNS 验证。
- **2. 算一次跑道**：可用余额 ÷ 月 burn = 跑道月数。这个除法比任何增长指标都早报警。
- **3. 读一遍你的定价页与合同**：什么会被收回、什么永久归你、最小档是不是 1–20 人的小团队也买得起。
- **4. 数一次你的付费转化**：付费转化常年为 0 的人，流量越大越危险。
 1W

### 如果你有一个周末

- **5. 做一次可迁移性体检**：订阅者/客户名单、内容、数据导出、第二分发渠道各一份；把「平台封禁我怎么办」写进应急预案第一页；列出每个第三方 API 的替代路径。
- **6. 换一次获客结构**：把内容预算从「写更多」换成「进第三方榜单与评测页」；先做一次归因体检，确认你的流量到底从哪来。
- **7. 重排你的成本与定价**：模型单价按同等准确率口径比价；最小档定价对照托管成本地板（自托管在 $2–3/月）；把按量计费的构建迁到固定成本机器。
 BET

### 如果你要押一个方向

- **8. AI 引用与转化归因**：需求信号清楚，一位独立开发者正在公开问，付费证据为零。可见度监测已有产品，成交归因仍待验证——先做自己的体检工具：谁在抓我、我有没有被引用、哪条答案带来了注册。
 明确不要做的
- AI 代码质量打分（本周没有可复现定义）
- 「给 AI 卖调用次数」的目录（中位收入 29 美分）

数据窗口：2026-11-15 至 11-21；分数与评论数为 2026-11-22 的记录时点值。金额均标注当事人自述、第三方统计或厂商口径；不构成成交证明。
