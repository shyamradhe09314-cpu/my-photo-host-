
# Create and configure a GitHub Pages repo that serves docs/img/photo.jpg.
# Requires env: GITHUB_TOKEN and optional REPO_NAME (default: my-photo-host).
#
# Steps:
# - Determine username from /user
# - Create repo (POST /user/repos)
# - Commit docs/.nojekyll, docs/index.html, docs/img/photo.jpg
# - Enable GitHub Pages (POST /repos/{owner}/{repo}/pages with source main + /docs)
import os, sys, base64, requests

API = "https://api.github.com"

def gh(token):
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return s

def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")

def put_file(session, owner, repo, path, content_bytes, message):
    # Check if file exists to include sha on update
    r = session.get(f"{API}/repos/{owner}/{repo}/contents/{path}")
    sha = None
    if r.status_code == 200:
        sha = r.json().get("sha")
    payload = {
        "message": message,
        "content": b64(content_bytes),
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha
    r = session.put(f"{API}/repos/{owner}/{repo}/contents/{path}", json=payload)
    r.raise_for_status()
    return r.json()

def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: Set GITHUB_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)
    repo_name = os.getenv("REPO_NAME", "my-photo-host")

    s = gh(token)

    # Who am I?
    me = s.get(f"{API}/user")
    me.raise_for_status()
    owner = me.json()["login"]

    # Create repo (idempotent: if exists, skip)
    r = s.post(f"{API}/user/repos", json={
        "name": repo_name,
        "description": "Static single-photo host via GitHub Pages",
        "private": False,
        "auto_init": True
    })
    if r.status_code in (201, 202):
        print(f"Created repo: {owner}/{repo_name}")
    elif r.status_code == 422 and 'already exists' in r.text.lower():
        print(f"Repo {owner}/{repo_name} already exists. Continuing...")
    else:
        r.raise_for_status()

    # Write files from local template
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, os.pardir))
    with open(os.path.join(root, "docs", ".nojekyll"), "rb") as f:
        put_file(s, owner, repo_name, "docs/.nojekyll", f.read(), "Add docs/.nojekyll")
    with open(os.path.join(root, "docs", "index.html"), "rb") as f:
        put_file(s, owner, repo_name, "docs/index.html", f.read(), "Add docs/index.html")
    with open(os.path.join(root, "docs", "img", "photo.jpg"), "rb") as f:
        put_file(s, owner, repo_name, "docs/img/photo.jpg", f.read(), "Add placeholder photo")

    # Enable GitHub Pages: source main + /docs
    r = s.post(f"{API}/repos/{owner}/{repo_name}/pages", json={
        "source": {"branch": "main", "path": "/docs"}
    })
    if r.status_code in (201, 204):
        print("Enabled GitHub Pages (main + /docs).")
    elif r.status_code == 409:
        print("Pages already configured. Skipping.")
    else:
        r.raise_for_status()

    site_url = f"https://{owner}.github.io/{repo_name}/"
    print("\n✅ Done! Your site should be live shortly:")
    print(site_url)
    print("Direct image URL (may 404 until uploaded/replaced):")
    print(site_url + "img/photo.jpg")

if __name__ == "__main__":
    main()
