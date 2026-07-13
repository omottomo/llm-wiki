# ai-llm-wiki Web Publishing Plan (Quartz 5 + Cloudflare Pages)

## Context

- The user maintains a Korean-language LLM wiki at `~/Desktop/ai-llm-wiki`, following karpathy's llm-wiki pattern (66 md files in `wiki/`: 20 concepts, 28 sources, 12 entities, 4 analysis + index/overview).
- Goal: publish the local wiki as a **public website** while preserving Obsidian-style visualization (graph view, backlinks, wikilinks).
- Note format: YAML frontmatter (`title/type/created/updated/sources/tags`), wikilinks in `[[concepts/hooks]]` and `[[...|alias]]` forms, no images. Link integrity is enforced by `scripts/lint_wiki.py`.
- Constraints: `raw/` contains full auto-generated transcripts of other people's YouTube videos → **must not be published on the web, and should not be exposed in a public repo either (copyright)**. The agent workflow (CLAUDE.md, skills) must keep working unchanged.
- Current state: git initialized (1 commit, `main`), **no remote yet**. Local Node is v20.19.5 (below Quartz 5's requirement).

## Tool Selection (based on web research)

**Chosen: Quartz 5** (https://quartz.jzhao.xyz/) — an open-source SSG purpose-built for publishing Obsidian vaults.

| Candidate | Assessment |
|---|---|
| **Quartz 5 (chosen)** | Free, open source. Graph view, backlinks, full-text search (official CJK tokenization), wikilinks + aliases, popover previews, tag pages, built-in ko-KR locale (verified: `quartz/i18n/locales/ko-KR.ts`) |
| Obsidian Publish | Official, but paid ($8–10/month) |
| Digital Garden plugin | Free, but UI polish is reportedly weak |
| MkDocs Material | No graph view / backlinks; poor fit for networked notes |

**Hosting: Cloudflare Pages (recommended)** — connects to a private GitHub repo + free + unlimited bandwidth + `*.pages.dev` subdomain. The only simple setup that keeps `raw/` private while giving automatic deploys. (GitHub Pages free tier requires a public repo → would expose `raw/`. A two-repo fallback is documented in §7.)

**Repo layout: monorepo** — vendor Quartz into `ai-llm-wiki/site/` (remove its `.git`, commit as regular files) and connect content via a **relative** symlink `site/content → ../wiki`. One repo, one `git push` deploys wiki + site together, zero changes to the existing agent workflow. (Verified in Quartz v5 CLI source that the symlink strategy supports relative paths.)

## Implementation Steps

### 1. Prerequisites — Node upgrade + private GitHub repo
```bash
nvm install 22 && nvm use 22        # or: brew install node@22 (requires Node >=22, npm >=10.9.2)
cd /Users/tomo/Desktop/ai-llm-wiki
gh repo create ai-llm-wiki --private --source=. --push   # MUST be --private (protects raw/)
```

### 2. Vendor Quartz + connect content
```bash
cd /Users/tomo/Desktop/ai-llm-wiki
git clone https://github.com/jackyzha0/quartz.git site && rm -rf site/.git
cd site && npm i
npx quartz create -X symlink -s ../wiki -l absolute
npx quartz plugin install --from-config
```
- Verify `site/content` is a **relative** symlink to `../wiki` (if absolute, replace with `ln -sfn ../wiki content` — absolute paths break in CI).
- `raw/`, `CLAUDE.md`, `AGENTS.md`, `log.md`, `.obsidian/`, `.claude/` live outside the content root (`wiki/`), so they are structurally excluded from publishing.

### 3. Edit `site/quartz.config.yaml` (v5 uses YAML config)
```yaml
configuration:
  pageTitle: "AI·LLM Wiki"           # adjust to taste
  locale: ko-KR                       # Korean UI / date formatting
  baseUrl: <project-name>.pages.dev   # must match the Cloudflare Pages project name
  analytics: null                     # default is plausible → turn off
  theme:
    typography:
      header: Noto Sans KR            # default theme fonts lack Korean glyphs
      body: Noto Sans KR
plugins:
  - source: github:quartz-community/crawl-links
    options:
      markdownLinkResolution: absolute   # resolves root-relative links like [[concepts/hooks]]
  - source: github:quartz-community/footer
    options:
      links: {}                          # remove default Quartz GitHub/Discord links
```
- `created`/`updated` frontmatter keys are natively supported as aliases by v5 core → no migration needed.
- graph/search/backlinks/explorer/tag-page plugins are enabled by default — leave as is. After editing, re-run `npx quartz plugin install --from-config` (updates `quartz.lock.json`; always commit the lockfile).

### 4. Local verification
```bash
cd site && npx quartz build --serve   # http://localhost:8080
```
(Checklist in the Verification section below.)

### 5. Commit & push
```bash
git status   # confirm site/node_modules, site/public, site/.quartz are ignored (Quartz ships a .gitignore)
git add site && git commit -m "Add Quartz 5 site scaffolding" && git push origin main
```

### 6. Connect Cloudflare Pages (CI/CD — every push auto-deploys afterwards)
Dashboard → Workers & Pages → Create → Pages → Connect to Git → select the private `ai-llm-wiki` repo:

| Setting | Value |
|---|---|
| Production branch | `main` |
| Root directory | `site` |
| Build command | `npm ci && npx quartz plugin install && npx quartz build` |
| Build output directory | `public` |
| Environment variable | `NODE_VERSION=22` |

- The project name becomes the subdomain → keep it consistent with `baseUrl` in §3; if they differ, fix the config and push again.
- Every page has frontmatter dates, so Cloudflare's shallow clone (inaccurate git dates) is a non-issue here.
- Custom domain is optional: Cloudflare Pages → Custom domains → add CNAME, then update `baseUrl` and redeploy.

### 7. Fallback (if Cloudflare Pages is not an option): GitHub Pages + two-repo split
Create a public repo `ai-llm-wiki-site` (Quartz + a real `content/` directory), and add a GitHub Action to the private wiki repo (`.github/workflows/publish-content.yml`) that rsync-pushes only `wiki/` into it (using a deploy key). The site repo uses Quartz's official v5 `deploy.yml` unchanged. **`raw/` never enters the public repo under any circumstances.**

### 8. Quartz upgrade operations (the vendoring trade-off)
Removing `.git` means `npx quartz update` is unavailable — when needed (rare), clone the new version to a temp dir and swap the code while preserving the config and the content symlink. Alternative: use git subtree from the start (`git subtree add --prefix=site ... v5 --squash`) to allow `git subtree pull` upgrades.

## Risks / Caveats

- **Node version**: local v20.19.5 is below the requirement — without the upgrade in step 1, even `npm i` may fail. Also set `NODE_VERSION=22` on Cloudflare.
- **raw/ copyright**: two layers of protection (private repo + content root limited to `wiki/`). Never accidentally flip the repo to public.
- **Korean search quality**: CJK tokenization is officially supported, but partial matching on particle-suffixed words (e.g. "하네스를") may be imperfect → verify with representative queries during local testing; if lacking, enrich `description` frontmatter.
- **Korean fonts**: default theme fonts have no Korean glyphs → set Noto Sans KR (§3). If the `og-image` plugin renders broken Korean in social images, disable just that plugin.
- **sources/ pages**: these are the user's own written summaries of others' videos, fine to publish; if undesired, switch to a whitelist model via the `explicit-publish` plugin (default: publish everything).

## Verification

**Local (localhost:8080)**
1. `/` renders `wiki/index.md` as the landing page; the `[[overview]]` link works
2. Korean search (⌘K): "하네스", "컨텍스트", "카파시" → title/body matches
3. Wikilinks: `[[concepts/hooks]]`, `[[...|하네스]]` alias display, `(→ [[sources/youtube-XXXX]])` citation links resolve
4. Graph view (local/global), backlinks panel, popover previews
5. Korean tag pages (URL-encoded) / Explorer folder tree / dates shown in Korean format
6. Mobile responsive + dark mode
7. **Output audit**: `grep -r "raw/" site/public/` returns nothing — confirm no transcript text is included

**Production (`*.pages.dev`)**
8. Re-check the items above + `sitemap.xml`/RSS use the correct baseUrl
9. Edit one wiki page → push → confirm Cloudflare auto-redeploys (2–3 min)
10. Final check that the GitHub repo is Private
