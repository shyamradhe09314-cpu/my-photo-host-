
# Upload (replace) or delete docs/img/photo.jpg in your GitHub Pages repo.
# Usage:
#   export GITHUB_TOKEN=...
#   export OWNER=<your-username>
#   export REPO=<your-repo-name>
#   python manage/photo_cli.py --upload /path/to/image.jpg
#   python manage/photo_cli.py --delete
import os, sys, base64, io, requests
from typing import Optional

try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

API = "https://api.github.com"
TARGET_PATH = "docs/img/photo.jpg"

def gh(token):
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return s

def b64(data: bytes) -> str:
    import base64 as _b
    return _b.b64encode(data).decode("utf-8")

def get_sha(session, owner, repo, path) -> Optional[str]:
    r = session.get(f"{API}/repos/{owner}/{repo}/contents/{path}")
    if r.status_code == 200:
        return r.json().get("sha")
    return None

def put_photo(session, owner, repo, img_bytes):
    sha = get_sha(session, owner, repo, TARGET_PATH)
    payload = {
        "message": "Upload/replace photo.jpg",
        "content": b64(img_bytes),
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha
    r = session.put(f"{API}/repos/{owner}/{repo}/contents/{TARGET_PATH}", json=payload)
    r.raise_for_status()
    return r.json()

def delete_photo(session, owner, repo):
    sha = get_sha(session, owner, repo, TARGET_PATH)
    if not sha:
        print("Nothing to delete (photo.jpg not found).")
        return
    r = session.delete(f"{API}/repos/{owner}/{repo}/contents/{TARGET_PATH}", json={
        "message": "Delete photo.jpg",
        "sha": sha,
        "branch": "main",
    })
    r.raise_for_status()
    print("Deleted docs/img/photo.jpg")

def to_jpeg_bytes(path):
    # If input is already .jpg/.jpeg, just read
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        with open(path, "rb") as f:
            return f.read()
    if not HAS_PIL:
        raise RuntimeError("Non-JPG given but Pillow not installed. Install with: pip install pillow")
    # Convert to JPEG (RGB)
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90, optimize=True)
    return buf.getvalue()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload", help="Path to local image to upload as photo.jpg")
    parser.add_argument("--delete", action="store_true", help="Delete photo.jpg from repo")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("OWNER")
    repo = os.getenv("REPO")
    if not token or not owner or not repo:
        print("ERROR: Set env vars GITHUB_TOKEN, OWNER, REPO", file=sys.stderr)
        sys.exit(1)

    s = gh(token)

    if args.delete:
        delete_photo(s, owner, repo)
    elif args.upload:
        img_bytes = to_jpeg_bytes(args.upload)
        put_photo(s, owner, repo, img_bytes)
        site = f"https://{owner}.github.io/{repo}/"
        print("✅ Uploaded!")
        print("Page:", site)
        print("Image:", site + "img/photo.jpg")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
