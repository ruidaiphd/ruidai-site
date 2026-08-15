# Getting the site live

Start to finish, about 20 minutes. Domain comes later — you'll have a working public URL
before you touch DNS.

Everything below is macOS Terminal. Copy one block at a time.

---

## Step 0 — Check what you already have

```bash
python3 --version
git --version
```

Both ship with macOS. If `git` prompts you to install developer tools, accept it and wait.
Anything Python 3.9 or newer is fine.

---

## Step 1 — Install the two dependencies

```bash
python3 -m pip install --user pyyaml markdown
```

If that errors with **externally-managed-environment**, use a virtual environment instead:

```bash
cd ~/Sites/ruidai            # do Step 2 first if this folder doesn't exist yet
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml markdown
```

With a venv you'll need `source .venv/bin/activate` each new Terminal session before building.

---

## Step 2 — Put the folder somewhere permanent

Move the `site` folder out of the Claude outputs directory — that gets cleared.

```bash
mkdir -p ~/Sites
mv ~/Desktop/site ~/Sites/ruidai      # adjust the source path to wherever you saved it
cd ~/Sites/ruidai
ls
```

You should see `build.py`, `content`, `templates`, `assets`, `docs`, `README.md`.

---

## Step 3 — Build

```bash
python3 build.py
```

Expected:

```
built  12 publications  1 working  4 projects  ->  docs/
```

If it prints `warn` lines, they're advisory. If it prints `ERROR` and stops, fix
`content/papers.yml` and run again — it deliberately writes nothing when the record is invalid.

---

## Step 4 — Look at it

```bash
open docs/home.html
```

The pages are self-contained, so opening the file directly works. Click through to Research,
try the UTD24 / FT50 pills, hover the coauthor graph.

To view it exactly as a server would:

```bash
python3 -m http.server 8000 -d docs
```

Then open <http://localhost:8000>. `Ctrl-C` to stop.

**Change something and rebuild** — this is the loop you'll use forever:

```bash
open -e content/home.md      # edit the "what I study" line
python3 build.py
open docs/home.html
```

---

## Step 5 — Put it under version control

```bash
cd ~/Sites/ruidai
git init -b main
git add -A
git commit -m "Initial site"
```

---

## Step 6 — Create the GitHub repository

In a browser: **github.com → + → New repository**.

- **Name:** `ruidai-site`
- **Public** — required for free GitHub Pages
- **Do not** add a README, .gitignore, or licence. The folder already has what it needs.

> You already own `ruidaiphd.github.io`. If you'd rather the site live at the root of that
> address, name this repo `ruidaiphd.github.io` instead — but that replaces whatever is
> currently published there. Either works; the custom domain in Step 9 makes the difference
> invisible.

Then, back in Terminal — GitHub shows these two lines on the new empty repo page:

```bash
git remote add origin https://github.com/<your-username>/ruidai-site.git
git push -u origin main
```

---

## Step 7 — Turn on GitHub Pages

In the repository: **Settings → Pages**.

- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/docs`
- **Save**

Wait about a minute, then reload the Settings → Pages screen. It shows your live URL:

```
https://<your-username>.github.io/ruidai-site/
```

That's the site, public, on HTTPS. **You're live.** Send it to someone and check it on a phone.

---

## Step 8 — The ongoing loop

From here, publishing anything is three commands:

```bash
cd ~/Sites/ruidai
python3 build.py
git add -A && git commit -m "add JFE paper" && git push
```

The site updates about a minute after the push. Adding a paper means editing
`content/papers.yml` — see README for the field list — and everything else follows: counts,
topic bars, the agenda chart, the coauthor network.

---

## Step 9 — The domain, whenever you're ready

Nothing above depends on this, and the site works fine without it.

1. Edit `content/site.yml`, add a line at the top:

   ```yaml
   domain: ruidai.info
   ```

   Then `python3 build.py` — this writes `docs/CNAME`, which is how GitHub Pages
   claims the domain. Commit and push.

2. At your domain registrar, add DNS records:

   | Type | Name | Value |
   |---|---|---|
   | CNAME | `www` | `<your-username>.github.io` |
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |

   *(Confirm the current apex IPs against GitHub's docs at the time you do this — they've
   changed before.)*

3. **Settings → Pages → Custom domain** — enter the domain, save, wait for the check to pass,
   then tick **Enforce HTTPS**. The certificate is automatic and free.

If you move to a new domain, keep `ruidaiwrds.info` renewing for two or three years with a
redirect, so links in your published papers keep resolving.

---

## Why GitHub Pages rather than Cloudflare

I originally suggested Cloudflare Pages for its unmetered bandwidth. Two things changed my
mind:

- **You need GitHub anyway** for the source. GitHub Pages means one account, one dashboard,
  one push — no second service to set up or remember.
- **Cloudflare is steering new projects away from Pages** toward Workers. Pages still works
  and isn't deprecated, but starting a brand-new project on the product they've stopped
  investing in is a poor bet.

The tradeoff is GitHub's 100 GB/month soft bandwidth limit. Your pages are about 180 KB, so
that's roughly 550,000 visits a month. If you ever approach it, putting Cloudflare's free CDN
in front is an afternoon's work and changes nothing about this workflow.

---

## When something goes wrong

| Symptom | Cause |
|---|---|
| `ModuleNotFoundError: yaml` | Step 1 didn't run, or the venv isn't activated |
| Build prints ERROR and stops | Invalid topic key or status in `papers.yml`; `docs/` is untouched |
| 404 at the Pages URL | Folder wasn't set to `/docs`, or the first build hasn't finished |
| Page loads unstyled | Fonts blocked by a network; harmless, layout still works |
| Changes not appearing | Forgot `python3 build.py` before committing |

The generated `docs/` folder is disposable — deleting it and rebuilding always works.
