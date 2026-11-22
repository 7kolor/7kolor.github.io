# 7Kolor Insights — 2026 W46 Weekly Report

## Three Threads of Business Intel: Who Pays, Who Holds Pricing Power, What Traffic Became

> The clearest payment signal came from noise evidence, with donation and replication intent; pricing power breaks over revocation; some search traffic is falling and AI citation is a new channel — this week's business intelligence.

原文 / Source: /weekly/2026-W46/

---

**The week in one line**: See who pays for what, write your pricing power into the contract, then swap write-more-content for get-cited.

> “OP, throw up a donation link I will give you some money if you want.”

 [the clearest payment signal this week](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/19sumrvcqav9h/) — the ask is submittable complaint evidence, not a device
- **Concrete payment signal**：1 · Community noise evidence: donation and replication intent for proof
- **Median monthly income, AI pay-per-use**：$0.29 · Across 1,536 services, unverified by a third party
- **The entry tier buyers couldn't buy**：100 · OpenCloud's lowest tier starts at 100 users
- **Year-over-year drop for one search term**：56% · html2pdf — the channel for utility SaaS is vanishing

**How to read this report**: if you only have 15 minutes, read Sections 1, 2 and 7; if you are looking for direction, Sections 3 and 4 are the wins and the mines; if you build products, skim the New Product Radar in Section 5.

  This issue at a glance  The three hardest calls this week [**The clearest payment signal came from evidence**Donation and replication intent appeared; recurring payment is unverified](#top3) [**The pricing landmine is not price**It is what gets revoked; willing buyers can't buy the 100-user tier](#top3) [**Search traffic is falling for some; AI citation is a new channel**The replacement is being cited; revenue attribution stays unverified](#top3)  Directions we rejected [**Selling calls to AI**1,536 samples, 29 cents median monthly income](#reject) [**Treating AI-citation monitoring as an empty market**Monitoring and assistant-traffic tools exist; revenue attribution is unverified](#reject)  Still waiting for evidence [**Attribution from AI answers to customers**Visibility monitoring exists; revenue attribution is unverified](#top3) [**Will utility SaaS be given away**Channel-side evidence only: html2pdf searches -56% YoY](#signals)

## 1. The Three Things That Mattered

 The clearest payment signal this week came from evidence; the pricing-power landmine is not price but what can be revoked; and some search-driven traffic is declining.      01

### The clearest payment signal came from noise evidence, with donation and replication intent

[the community noise-evidence thread](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/): the poster records noise with a $30 clearance tablet to file with the city, and the comments hold all three at once — people offering to pay, people wanting to copy it, people asking where to buy the hardware.

**The ask is submittable complaint evidence, not a device**

> “OP, throw up a donation link I will give you some money if you want.” (u/Hasz, 42 pts);

> “i would be very interested in mimicking this project.” (u/dope_zebra, 52 pts).

 First test whether users will keep paying for submittable complaint evidence; only then build capture, local classification and one-click export.

**The counter-sample the same week: 1,536 pay-per-use AI services**About $40k in total, the top 7 took ~$30.5k, the other 1,529 shared ~$9.8k, median seller income 29 cents, 1,034 made under $1 for the month, and roughly a third never delivered. The flaw is unit value below unit cost, not pay-per-use itself; the positive sample priced a per-call action that produces real ranking, at $3 an article.

**Move**Write one sentence on why a customer pays — the answer must contain a deliverable result, not a feature. Price your smallest billable unit at a multiple that covers one delivery. If you are eyeing AI pay-per-use micro-services, read the median before the mean.

  02

### Customers pay for ownership and leave over revocation — three cases, one spot

[Infisical paywalled custom roles in a patch release](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/): the paywall landed on the one thing that limits what a machine identity can do — in a secrets manager that means zero permission management.

**Trust collapses in three steps**Step one, a breaking change ships in a patch; step two, docs change quietly before release notes; step three, a willing buyer cannot find sales:

> “The sales person said it wasn't possible… then they stopped responding. It is not a serious company.” (u/_f0CUS_, 95 pts).

The reaction is not “expensive” — it is “you don't understand why I'm here.”

**Willing buyers can't find a tier to buy**OpenCloud's move to subscription did not itself backfire — the tiers did:

> “Im interested in the Basic subscription also to support the project but on the pricing page it says starting from 100 users.” (u/siegfriedthenomad, 8 pts) — a small team that wants to pay cannot find a tier.

**Upstream price hikes produce migration, not payment**[Last.fm ties its API to Pro](https://www.reddit.com/r/selfhosted/comments/1xzka97/lastfm_api_keys_will_require_pro_from_1st_december/):

> “$4.99 a month. GTFO. I'll just subscribe to Spotify again” (u/SolFlorus, 214 pts). When a product can be rewritten over a weekend, price loses its floor:

[“a cloned app has no floor at all” — u/drakatmm](https://www.reddit.com/r/micro_saas/comments/1xzgs3p/saas_as_we_know_it_is_dying_and_wispr_flow_is_the/19sv8nc2oveud/)

 This week's price points in the same threads: seller revenue and cost vs customer payments and platform cuts

Figures: seller side — $0.29, $29, $215 → $4, $2–3/mo; customer and platform side — $4.99/mo, ~30%, $100/mo, entry at 100 users.

**Move**Put “what you own forever, what can be revoked” into your pricing page and contract. Keep a 1–20 person tier — never start at 100 users. For every third-party API, write down the replacement path for the day it reprices or bans you; no path means single-point risk.

  03

### Search traffic is declining for some; AI citation is a new channel

[the search-traffic -40% thread](https://news.ycombinator.com/item?id=50540178)— and the poster is slashdev: the 40% comes from a third-party study, not community consensus. Measured outcomes in the comments are worse: “My traffic is down over 80%. … By December next year I'll probably have to put the website in maintenance mode and find another job.” (u/nicbou).

**The counterpoint belongs here: demand did not vanish, the channel moved**Falling search traffic does not mean falling demand —

> “our sign up rate and conversions are significantly higher. AI feeds in better leads than just a single search query.” (u/robeym), plus a case of cold clients arriving straight from ChatGPT (u/komali2).

And do not write off the engine that still works: one indie developer drew eight to nine of ten signups from SEO and AEO this period, converting about 3%.

**AI citation is a new channel; attribution is still unverified**The clearest demand signal is a founder asking in public, “How to gain visibility in AI tools like chatGPT?”, with 72 comments of answers:

> “One mention in a well-trafficked listicle beats ten posts on your own blog.” (u/cethu3001, 6 pts). Be honest though: visibility monitoring and assistant-traffic measurement already exist; which answer produced a signup or a sale remains an unverified question, not a proven gap —

> “no public dashboard shows who references your brand in their answers” (u/brilliantzen, 1 pt, same thread); the same comment promotes the author's related tool, so treat it as a lead rather than market proof.

**Move**Four things today: claim your domain, check whether robots.txt or Cloudflare blocks AI crawlers by default, put positioning and pricing in plain text, then probe whether you are cited. Move content budget from “write more” to “get into third-party lists”. If search is your main channel, run an attribution check before rewriting your content strategy.

## 2. Five Pains That Land on Operations

 All five pains land on money: channel, pricing power, tier design, single-point dependency, unit economics. Each carries a mechanism, an action for today, and who it applies to.

#### 1. Distribution: the traffic mix is shifting, AI attribution is unverified

 −80%One creator's measured drop370/400Bots out of 400 homepage hits−56%html2pdf searches, YoY

[How to gain visibility in AI tools](https://www.reddit.com/r/Entrepreneur/comments/1xyitwp/how_to_gain_visibility_in_ai_tools_like_chatgpt/): Some search-dependent sites are losing traffic as AI answers take the read-the-answer visits, indexing slows and crawlers dilute the rest. AI citation is a new channel; which answer produced a customer is still unverified.

 Flip for the move to copy →

##### Move to copy

Four moves: claim your domain, check crawler blocking, write a plain-text positioning page, probe whether you are cited. Move content budget from write-more to get-into-third-party-lists.

Applies to: Anyone acquiring customers through search and content

Source: [source](https://www.reddit.com/r/Entrepreneur/comments/1xyitwp/how_to_gain_visibility_in_ai_tools_like_chatgpt/)

#### 2. Pricing power you don't have: upstream hikes arrive as migration

 $4.99Upstream API monthly fee160“Another dirty corporation fronting as open source”13Comments saying they already migrated

[the Infisical paywall case](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/): Upstream price hikes rarely arrive as a price rise; they arrive as switch-or-shut-down. A paywall shipped in a patch does not cost you the feature — it costs the community's stars, PRs and answers, which is where early growth came from.

 Flip for the move to copy →

##### Move to copy

For every third-party API, write down the replacement path for the day it reprices or bans you; no path means single-point risk. For your own product: never let the free tier lock the migration path, and never put the paywall on the feature users care most about.

Applies to: Anyone on someone else's API, and anyone selling to users

Source: [source](https://www.reddit.com/r/selfhosted/comments/1xwoq7y/infisical_paywalled_custom_roles_for_selfhosters/)

#### 3. Trust broken unilaterally: willing buyers can't find a tier

 100OpenCloud's entry tier starts at95The willing-buyer comment's score13Comments already migrated to OpenBao

[OpenCloud locks production into subscription](https://www.reddit.com/r/selfhosted/comments/1xzj6gq/opencloud_the_nextcloudowncloud_alternative/): Subscription itself did not backfire — tiers did: the entry tier starts at 100 users, so a small team that wants to pay cannot. Advance notice for breaking changes and a free tier that never locks the migration path are the actual floor of tier design.

 Flip for the move to copy →

##### Move to copy

Keep a 1–20 person tier; announce breaking changes in advance; ship the migration script before the subscription pitch.

Applies to: Anyone selling software to developers and small teams

Source: [source](https://www.reddit.com/r/selfhosted/comments/1xzj6gq/opencloud_the_nextcloudowncloud_alternative/)

#### 4. Single-platform dependency: one ban wipes the slate

 3,000+Subscriptions after eight months$0.76Available balance in another case~30%Marketplace commission plus fees

[the Substack suspension](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/): Failure is a consequence problem, not a probability problem: your assets sit inside someone else's rule system, appeals are a one-shot black box, and the channel itself becomes a cost line — commission plus fees around thirty percent, plus a subscription.

 Flip for the move to copy →

##### Move to copy

Three backups: the list, the content, the payment channel. Then one second distribution channel, a first page titled what-if-the-platform-bans-me, and a break-even GMV calculation before joining any marketplace.

Applies to: Anyone who acquires customers on one platform

Source: [source](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/)

#### 5. Unit economics and scale limits: traffic-revenue decoupling alarms first

 $0.29Median monthly income of 1,536 services$19.56clipr.cc's four-year total revenue$0.76LinkGenius's available balance

[LinkGenius's Stripe dashboard](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/): Traffic-revenue decoupling and fixed costs peaking first are the two earliest signals. The most under-estimated costs in a small business are time, chargebacks and cross-border fixed fees.

 Flip for the move to copy →

##### Move to copy

Runway = balance ÷ monthly burn; read the median, not the mean; reprice when fixed costs exceed 100% of potential revenue. Chargeback defense: a bill descriptor customers recognise, refund-small-first so it never becomes a dispute, batch cross-border payments.

Applies to: Every small business

Source: [source](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/)

## 3. Money & People: Payment Signals and Failure Samples

 No sales are claimed here: payment intent, pricing and cost samples, and failure cases stay separate. The shared early signals are unit economics and migration cost. W1

#### [a $30 tablet recording noise](https://www.reddit.com/r/selfhosted/comments/1xzus66/target_was_selling_a_android_tablet_for_30_so_im/)

“OP, throw up a donation link I will give you some money if you want.” — u/Hasz

 **Why it matters**The comments show donation, replication and hardware-purchase intent; that is interest, not proof of recurring payment. **What blocks it**Microphone auto-gain makes decibel readings untrustworthy, cheap hardware is unsustainable, and admissibility is unproven. **Copyable if**First test whether tenants, owners and residents' committees will pay for submittable complaint evidence; the device is only the capture step, not the product.  W2

#### [RankSpot](https://www.producthunt.com/posts/rankspot-2)

Priced at $3 per article, $0.004 per prompt check — vendor-reported

 **Why it matters**Pay-per-use works where the unit of work is expensive and ranks matter — not where free alternatives exist, like a weather API. **The counter-sample**The same week: 1,536 comparable services, median seller income 29 cents a month. **Copyable if**Every call you sell produces a metered result — not one more API relay.  W3

#### [Codemany](https://www.producthunt.com/posts/codemany-2)

$215 in October → $4 by mid-November — vendor-reported

 **Why it matters**Putting the invisible bill on the table is the product: developers finally see what CI costs them. **Caveat**One sample only; runner counts, minutes and specs are undisclosed, so it is not a budget you can copy. **Copyable if**Your product hides a cost your users can see once you draw it.  W4

#### [the income distribution of 1,536 services](https://www.reddit.com/r/passive_income/comments/1xwqicl/i_looked_at_what_1536_tiny_ai_pays_per_use/)

The top 7 took ~$30.5k; the other 1,529 shared ~$9.8k; the median seller made 29 cents — author's unverified analysis

 **Why it matters**When a category's income distribution is scarce information, the distribution lets readers judge a category; it is public evidence, not revenue proof. **How to use it**Look at the total, then the median, then head concentration, then the failure rate. **Copyable if**You can continuously and openly measure a market everyone joins but nobody measures.  Failure cases by size (log scale; amounts are self-reported) L1

#### clipr.cc: 10M visits in four years, $19.56 of revenue

Traffic and revenue decoupled: about 15k redirects a day and 150 daily users, with zero paid conversion for years. The early signal was fixed costs exceeding potential revenue, not a lack of traffic.

Source: [thread and numbers](https://www.reddit.com/r/SideProject/comments/1xx5n46/never_build_a_url_shortener_never/)

 L2

#### LinkGenius: eight months, $29 MRR and $0.76 available

Monthly burn was $130–170. Balance ÷ burn gives runway in months; when free and paid tiers do the same thing, pricing has removed the reason to pay.

Source: [the Stripe self-report](https://www.reddit.com/r/SaaS/comments/1xwno2k/i_started_building_my_saas_in_april_months_later/)

 L3

#### Substack: 3,000+ subscribers, wiped out by one ban

The first comment asked whether posts and the subscriber list were backed up. No case ID and a minute-fast rejection mean that even a thorough appeal may have no second channel.

Source: [the suspension self-report](https://www.reddit.com/r/Substack/comments/1xxbjzi/substack_suspended_my_account_and_denied_2/)

 L4

#### 1stDibs: channel costs ate the seller's margin

Commission plus payment fees came to roughly 30%, before a monthly subscription and ads. Calculate break-even GMV before joining; marketplace traffic alone is not a business case.

Source: [the seller-exit account](https://www.reddit.com/r/Flipping/comments/1xx51w2/1stdibs_a_marketplace_that_has_lost_its/)

 L5

#### Cold start: 50 targeted emails, zero replies

The comments named the sample problem: “Fifty emails is a sample size of basically zero.” Set the sample size before judging the channel, and write business outcomes rather than category labels.

Source: [the cold-start account](https://www.reddit.com/r/automation/comments/1xznabq/is_ai_automation_dead_has_every_business_in_the/)

 L6

#### AI-built sites: delivery revenue turns into maintenance debt

Time saved on delivery returns as plugin compatibility, testing and upgrade debt. Custom code without a test suite leaves maintenance responsibility with whoever delivered it.

Source: [the maintenance discussion](https://www.reddit.com/r/Wordpress/comments/1xzehba/wordpress_will_be_fine_what_happens_to_builders/)

 clipr.cc: 10M visits in four years, $19.56 revenue. LinkGenius: 8 months, $29 MRR, $0.76 left. Substack: 3,000+ subscribers, zero after one ban. 1stDibs: ~30% channel cost pushed sellers out. Cold outreach: 50 targeted emails, zero replies. AI-built sites turn into maintenance debt.

## 4. Directions We Rejected

 What we reject is a reading, not a need: each item carries the condition under which it still holds.

### Selling calls to AI: 1,536 samples say this is not an opportunity

[the income distribution](https://www.reddit.com/r/passive_income/comments/1xwqicl/i_looked_at_what_1536_tiny_ai_pays_per_use/): The author measured what these small services actually earned in October 2026.

**Mechanism: **Pay-per-use assumes demand up front: that an AI agent market willing to pay per call exists. This week's data says demand has not arrived while supply already numbers 1,536.

**The counterpoint: **Pay-per-use itself is fine — the positive sample this week priced a per-call action that produces real ranking, at $3 an article.

**Move: **Do not build the directory; first price what one call is worth against what it costs you to serve.

 Income buckets for 1,536 pay-per-use services (log scale; operator-computed, unverified)

Buckets: under $1: 1,034; $1–10: 360; $10–100: 113; above $100: 29.

### Scoring AI code quality: the most overestimated opportunity of the week

[the code-review bottleneck thread](https://news.ycombinator.com/item?id=50538303): The thread asks for measurable quality metrics and questions whether such a metric can be defined at all.

**Mechanism: **The highest-scoring comments all ask for a measurable quality metric — and the objections are just as clear: “Untested code is broken code”; without a defined architecture and conventions, agents are guessing; and the original data may not represent solo builders.

**The counterpoint: **What you can do is not scoring: feed review history back, encode your team's conventions, track miss rate.

**Move: **There is not enough evidence to start this; revisit next week and do not build on it before a reproducible definition exists.

## 5. New Product Radar

 Developer tools and agent infrastructure are still the thickest cluster, but the centre of gravity moved from billing to testing, verification, memory and identity. Use this layer as a supplier, not a rival. Category map of this week's launches (no counts, no votes, no rankings)

| Product | What it does | Why it’s worth a look |
|---|---|---|
| [Tabstack by Mozilla](https://www.producthunt.com/posts/tabstack-by-mozilla-2) | Research and browser automation as a hosted API, with the browser running outside your model; the vendor stresses never trained on, private by default | The only large-vendor-backed privacy-first capture layer of the week |
| [Puffin](https://www.producthunt.com/posts/puffin-2) | A dedicated email address, chat seat and calendar for every AI agent | Agent identity became a category of its own |
| [StateWeave](https://www.producthunt.com/posts/stateweave-2) | Agents run inside stateful clones of your apps, with injectable outages and 401s | Failure environments as infrastructure — exactly the gap in Section 1 |
| [Codemany](https://www.producthunt.com/posts/codemany-2) | Run GitHub Actions on your own infrastructure, with your own bill on display | Puts CI cost on the table; one sample, no baseline |
| [Privacyboard](https://www.producthunt.com/posts/privacyboard) | Detects third-party tools and drafts your privacy policy, cookie banner and DPA | Compliance is a market where someone already stepped on the mine |
| [RankSpot](https://www.producthunt.com/posts/rankspot-2) | A pay-per-use SEO and AI-search execution layer at $3 per article | The right use of pay-per-use: high-value actions with real rankings |
| [AI Context Flow MCP](https://www.producthunt.com/posts/ai-context-flow-mcp) | One shared memory across agents and teams over MCP | Cross-tool memory fragmentation is now its own category |
| [Glassmail](https://www.producthunt.com/posts/glassmail) | A Mac mail client whose AI runs entirely local — no subscription, one-time purchase | Local AI plus one-time purchase, echoing this week's backlash against paywalls |

## 6. Signals Worth Noting

 Sorted by business impact Hits revenue now

[utility SaaS is being commoditized, channel first](https://www.reddit.com/r/SaaS/comments/1xyg2q6/my_saas_makes_25kmonth_but_im_not_sure_it_has_a/)a €2.5k/month PDF API keeps its old customers but cannot find new ones; the comments point at the channel with data — “Search for "html2pdf" is down 56% YoY … Devs ask Claude instead of Google now.” (u/zggb, 24 pts).

[high-pay gig recruiting posts are a referral business](https://www.reddit.com/r/RemoteWorkers/comments/1xxf2tt/get_paid_45hour_to_help_train_ai_no_programming/)one account, two posts, one referral code, five hundred comments of applicant chatter and not one discussing the job — readers think you are selling a job; you are earning a referral fee.

 Changes pricing & contracts

[buyout vs usage rights is the core pricing trap](https://www.reddit.com/r/business/comments/1xzg87e/tesla_will_sell_you_a_cybercab_for_30000_then/)the anger is not the price; it is “I bought it and can't earn with it” — u/consultinglove, 111 pts.

[free model APIs must never face paying users](https://www.reddit.com/r/SaaS/comments/1y08vva/i_made_17k_usd_from_my_saas_and_here_are_the/)of 428 third-party API routers studied, 9 injected malicious code into responses and 17 touched planted credentials — a trust line, not a savings line.

[hosting cost floor is $2–3 a month](https://www.reddit.com/r/selfhosted/comments/1xy63oj/a_23mo_vps_is_the_best_remote_access_solution/)a $36/year machine is the cost floor for self-hosting — which is what finally makes “self-hosted / local / one-time purchase” viable.

 Product selection

[the retention switch for self-hosting is a concrete device](https://www.reddit.com/r/selfhosted/comments/1y1epug/be_honest_whats_the_selfhosted_service_you_spent/)“Getting an epson scanner to drop to the watch folder over SMB was what made me use it all the time.” The product is hardware + one-click setup + local search, not the software.

[signups are a vanity metric](https://www.reddit.com/r/SaaS/comments/1xz6qzx/i_just_crossed_15000_signups_in_my_saas_today/)15,000 signups converting ~3%; the comments agree the funnel leaks right after signup — “teams obsess over top of funnel while the real leak is that first 5 minutes after signup and the first week after.”

## 7. Last Issue’s Calls, Re-Checked

| Last issue’s call | Evidence this issue | Verdict |
|---|---|---|
| Set a cap before taking client work | The reverse case: AI-managed upgrades fail half as often but run ten times faster, so incidents per month go up fivefold (u/tflinton) | Upheld — make verification part of delivery |
| Price inside the range the buyer left you | Last.fm tied its API to Pro at $4.99 a month, pushing downstream users to migrate; Infisical's paywall landed on the one feature users could not lose | Upheld, plus one layer — prepare an alternative before upstream repricing |
| Don't pay for emotion | Payment intent appeared in several places: a noise-evidence donation, an Infisical sales failure and an OpenCloud tier gap; none is evidence of a completed sale | Upheld |
| Treat the agent billing layer as a supplier | Billing and usage products shrank in this week's launches; attention moved to developer tools and agent infrastructure; Codemany put its CI bill on display | Upheld, but the slot moved from billing to testing, verification and release orchestration |
 Last issue we wrote that AI code gets “fragile”. This week we correct it: fragility is the symptom, the queue is the mechanism — as output gets cheaper, cost moves to verification bandwidth, and bandwidth does not widen by itself. Last issue we called the AI gig-platform rejection “oversupply”; the sharper version is that oversupply is the symptom and unit value below unit cost is the mechanism.

## 8. This Week’s Actions

 2H

### If you only have 2 hours

- **1. Check AI crawler blocking**: confirm robots.txt and Cloudflare are not blocking AI crawlers by default; put positioning and pricing on a plain-text page; claim your business in ChatGPT — free, DNS-verified.
- **2. Compute your runway**: available balance ÷ monthly burn = months of runway. This division alarms earlier than any growth metric.
- **3. Re-read your pricing page and contract**: what can be revoked, what is permanently yours, whether the smallest tier is affordable for a 1–20 person team.
- **4. Count your paid conversions**: if paid conversions have long been zero, more traffic is more danger.
 1W

### If you have one weekend

- **5. Run a portability check**: one copy each of your subscriber list, content, data exports and a second distribution channel; a first page titled what-if-the-platform-bans-me; a replacement path for every third-party API.
- **6. Restructure your acquisition**: move content budget from write-more to get-into-third-party-lists; run an attribution check to see where your traffic actually comes from.
- **7. Re-rank costs and pricing**: price models at equal accuracy on your own tasks; set the entry tier against the hosting floor (self-hosting at $2–3/mo); move metered builds onto fixed-cost machines.
 BET

### If you are betting on one direction

- **8. AI visibility attribution**: visibility monitoring and assistant-traffic measurement already exist; revenue attribution remains unverified. Run a small free test on your own site before treating this hypothesis as a product opportunity.
 Explicitly do not
- Scoring AI code quality (no reproducible definition)
- A pay-per-use directory for AI (median income 29 cents)

Window: 2026-11-15 to 11-21. Scores and comment counts are point-in-time values recorded on 2026-11-22. Amounts are labelled self-reported, third-party estimates or vendor-reported; none proves a completed sale.
