# ruidai.info — source

Everything on the site comes from `content/`. Nothing in `docs/` is ever edited by hand.

```
content/papers.yml     the publication record
content/site.yml       name, titles, links, topics, journal lists
content/home.md        the "what I study" paragraph
content/work.md        Data & tools projects
content/teaching.md    Teaching
assets/                banner.jpg, portrait.jpg, project screenshots
        ↓  python3 build.py
docs/                  generated — this is what gets deployed
```

## One-time setup

```bash
pip install pyyaml markdown
```

That's the whole dependency list. No Node, no framework, no lockfile.

## The loop

```bash
python3 build.py          # regenerate docs/
open docs/home.html       # check it
git add -A && git commit -m "add Management Science paper" && git push
```

The push is the deploy. GitHub Pages picks it up and the site is live in about a minute.

## Adding a paper

Open `content/papers.yml`, copy an entry, edit it:

```yaml
- title: Some New Paper About Disclosure
  year: 2027
  venue: Journal of Financial Economics
  volume: Vol. 150(2), 200-240      # leave '' if not yet assigned
  status: Published                  # Published | Forthcoming | Working paper
  lists: [ft50, utd24]               # [] if on neither list
  topics: [sc, ml]                   # keys from site.yml
  coauthors: [Lilian Ng, Hao Liang]
  url: https://doi.org/...
  notes: [Best paper, AFA 2027]      # awards, media, conferences
```

Run `build.py`. That single entry updates, with no other edits:

- the publications list and its numbering
- the **All / UTD24 / FT50 / Other** counts
- the topic bars
- the agenda lane chart, including the year axis if it extends the range
- the coauthor network and the ranked collaborator list
- the search index

Moving a paper from working to published means changing `status` and moving the entry from
`working:` to `papers:`. That's it.

## Adding a project to Data & tools

Add a `## Heading` block to `content/work.md`. Optional `kick:` and `url:` lines, then prose
in normal markdown. Drop `assets/<slug>.jpg` next to it — matching the slugified heading —
and the real screenshot replaces the generated placeholder panel.

## What build.py checks

Before writing anything it validates the record and **stops on errors**, leaving `docs/`
untouched rather than publishing something broken:

| | |
|---|---|
| **error** | unknown topic key, unknown journal list, invalid status |
| **warn** | missing URL, coauthor with no first name, one surname under two spellings |

That last warning matters more than it looks: `Ng` and `Lilian Ng` would silently become two
separate people in the coauthor network. It caught exactly that during testing.

## Notes on the output

Publication rows are rendered into the HTML **at build time**, not only by JavaScript. Search
engines and anyone with JS disabled see the full list of titles, authors, and venues. The
script then takes over for filtering and the network graph. This matters — the main reason to
leave Google Sites is that people should find this page when they search your name.

Images are embedded as base64 so each page is a single self-contained file. Copies also live
in `docs/assets/` if you'd rather link them externally later.

---

# Hosting

**Step-by-step launch instructions are in [LAUNCH.md](LAUNCH.md).**

## Recommendation

| Layer | Where | Cost |
|---|---|---|
| Static site (`docs/`) | **GitHub Pages**, served from `/docs` on `main` | free |
| TLS | GitHub, automatic | free |
| Domain | registrar of choice | ~$12–15/yr |

**The hosting is free.** The domain is the only recurring cost, and if you keep
`ruidaiwrds.info` the marginal cost of launching is zero.

There is no server. Nothing to patch, no OS updates, no TLS renewal, no Docker, no bill that
grows. The site is files on a CDN.

GitHub Pages, rather than Cloudflare Pages, for two reasons: you need GitHub anyway for the
source, so this adds no second account or dashboard — and Cloudflare has stopped investing in
Pages in favour of Workers, which makes it a poor product to *start* a new project on.

The tradeoff is GitHub's 100 GB/month soft bandwidth limit against Cloudflare's unmetered. At
~180 KB per page that's roughly 550,000 visits a month. If you ever approach it, putting
Cloudflare's free CDN in front is an afternoon and changes nothing about this workflow.

## Setting it up

See [LAUNCH.md](LAUNCH.md) for the full walkthrough. In short: push this folder to a public
GitHub repo, then **Settings → Pages → Deploy from a branch → `main` / `/docs`**.

`docs/` is committed on purpose. GitHub *can* run the build in an Action, but committing the
output means the deploy has no moving parts — no build image, no Python version pin, nothing
that breaks in eighteen months while you're not looking. You already run `build.py` locally to
preview; commit what you previewed.

If you'd rather not commit generated files, add a GitHub Action running `python3 build.py`.
It's a real tradeoff, not an obvious win.

## The domain

`ruidaiwrds.info` encodes an affiliation that's now secondary. Since you're rebuilding anyway,
this is the cheap moment to move to something name-based. Keep the old domain renewing 2–3
years with a 301 redirect so links in your published papers keep resolving — about $15/yr to
protect a decade of citations.

## If the WRDS appendix link ever dies

Not hosting the novelty appendix is the right call — it's the only thing that would have
required a server, and it's WRDS infrastructure, not yours.

Worth knowing the one exposure it leaves. `wrds-rd-demo.wrdscloud.com:8000` is cited in the
*Review of Finance* paper, and a published PDF can't be patched. If that host is ever retired,
the citation breaks permanently.

The zero-cost hedge, whenever convenient: a static `appendix.html` page in this site — a few
screenshots of the interface, the underlying data as a download, and a short description of
what the tool did. It's a normal page in `content/`, costs nothing, and means the paper's
reference resolves to something real regardless of what happens to the WRDS box. No server
involved. Only worth doing if and when the link actually goes.

## Sources

- [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits)
- [Cloudflare Pages pricing and bandwidth, 2026](https://www.devtoolreviews.com/reviews/cloudflare-pages-pricing-bandwidth-limits-2026)
- [Static host comparison, 2026](https://htmlpub.com/blog/static-site-hosting-comparison-2026)
- [Cloudflare: migrate from Pages to Workers](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/)
- [GitHub Pages: configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
