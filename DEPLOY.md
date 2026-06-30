# Deploying TrustMed to Streamlit Community Cloud

The app runs two processes — the Streamlit frontend and the FastAPI backend.
On Streamlit Cloud, `frontend.py` automatically starts the backend in the same
container (see `_ensure_backend`), so you only deploy one app.

## 1. Put the project on GitHub

This folder is not a git repo yet. From the project directory:

```bash
git init
git add .
git commit -m "TrustMed: deploy-ready"
```

Then create an EMPTY repo on github.com (no README), and:

```bash
git remote add origin https://github.com/<you>/trustmed.git
git branch -M main
git push -u origin main
```

`.gitignore` already excludes `.env`, `*.db`, `venv/`, and `.streamlit/secrets.toml`,
so your API key is never pushed. Confirm with `git status` that none of those appear.

## 2. Set a spending cap FIRST (important)

In the Anthropic Console (console.anthropic.com) → Billing / Limits, set a monthly
usage limit on the key you will deploy with. A public URL backed by your key means
anyone who reaches it can spend your credits — the password below helps, but a cap
is your real backstop.

## 3. Create the Streamlit app

1. Go to https://share.streamlit.io and sign in with GitHub.
2. "Create app" → pick your repo, branch `main`, main file **`frontend.py`**.
3. (Advanced settings) Python version **3.11** or **3.12**.

## 4. Add secrets

In the app's "Secrets" box paste:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
APP_PASSWORD = "choose-a-strong-passphrase"
```

Deploy. The first load takes ~30s while the backend starts. Share the URL plus the
password with your testers.

## Notes / limits

- **Data is ephemeral.** `trustsim.db` resets whenever the app restarts or redeploys.
  For pilot data, have participants use the per-session JSON/CSV export on the
  Reflection page, or move storage to a managed database (e.g. Postgres) later.
- **One container.** Both processes share it; fine for a pilot. For always-on use
  with persistent data, move to a Docker host (Render/Fly) instead.
- **Updating the app:** push to `main`; Streamlit Cloud redeploys automatically.
