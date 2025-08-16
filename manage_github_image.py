import base64, json, os, sys, requests
GITHUB_API = "https://api.github.com"

def get_sha(owner, repo, path, token, branch="main"):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    r = requests.get(url, headers={"Authorization": f"token {token}", "Accept":"application/vnd.github+json"})
    if r.status_code == 200:
        return r.json().get("sha")
    if r.status_code == 404:
        return None
    raise SystemExit(f"Failed to get SHA: {r.status_code} {r.text}")

def upload(owner, repo, path, local_path, token, message="Upload/replace image", branch="main"):
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")
    sha = get_sha(owner, repo, path, token, branch)
    payload = {"message": message, "content": content, "branch": branch}
    if sha: payload["sha"] = sha
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    r = requests.put(url, headers={"Authorization": f"token {token}", "Accept":"application/vnd.github+json"}, data=json.dumps(payload))
    if r.status_code in (200,201):
        print("✅ Uploaded:", path)
    else:
        print(r.text); raise SystemExit("Upload failed")

def delete(owner, repo, path, token, message="Delete image", branch="main"):
    sha = get_sha(owner, repo, path, token, branch)
    if not sha:
        print("⚠️ Nothing to delete (file not found)."); return
    payload = {"message": message, "sha": sha, "branch": branch}
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    r = requests.delete(url, headers={"Authorization": f"token {token}", "Accept":"application/vnd.github+json"}, data=json.dumps(payload))
    if r.status_code == 200:
        print("🗑️ Deleted:", path)
    else:
        print(r.text); raise SystemExit("Delete failed")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("upload","delete"):
        print("Usage:\\n  python manage_github_image.py upload <owner> <repo> <token> <local_image> [remote_path=img/photo.jpg] [branch=main]\\n  python manage_github_image.py delete <owner> <repo> <token> [remote_path=img/photo.jpg] [branch=main]")
        return
    cmd = sys.argv[1]
    owner, repo, token = sys.argv[2], sys.argv[3], sys.argv[4]
    if cmd == "upload":
        local = sys.argv[5]
        remote = sys.argv[6] if len(sys.argv) >= 7 else "img/photo.jpg"
        branch = sys.argv[7] if len(sys.argv) >= 8 else "main"
        upload(owner, repo, remote, local, token, branch=branch)
    else:
        remote = sys.argv[5] if len(sys.argv) >= 6 else "img/photo.jpg"
        branch = sys.argv[6] if len(sys.argv) >= 7 else "main"
        delete(owner, repo, remote, token, branch=branch)

if __name__ == "__main__":
    main()
