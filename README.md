# my-photo-host

A tiny GitHub Pages repo that always shows `img/photo.jpg` at a fixed link. Replace or delete the file anytime to control what appears.

---

## Step-by-step (Mobile-friendly UI)

1) **GitHub par naya repo banao** (name: `my-photo-host`).
2) Is ZIP ko extract karo aur sab files upload karo.
   - Files honi chahiye:
     - `docs/index.html`
     - `img/` folder (andar `.gitkeep` ya aapka `photo.jpg`)
     - `.nojekyll`
     - `scripts/` (optional helper tools)
3) **Pages enable karo**  
   - Repo → Settings → Pages → Source: *Deploy from a branch* → Branch: `main`, Folder: `/docs` → Save.
4) **Live link**  
   - `https://<your-username>.github.io/my-photo-host/`
5) **Photo dikhana**  
   - `img/` folder me `photo.jpg` upload karo. Bas! Page par photo dikhegi.
6) **Photo replace**  
   - Dubara `img/photo.jpg` ko naya photo se replace kar do. Page refresh karte hi new photo.
7) **Photo delete**  
   - `img/photo.jpg` ko delete kar do → page par “Photo not found” message aayega.

---

## Alternative: Laptop se push (git)

```bash
# 1) Repo create karo GitHub pe (empty)
# 2) Iss folder me aa kar:
chmod +x scripts/push.sh
./scripts/push.sh <your-username> my-photo-host
# 3) Settings → Pages enable (branch: main, folder: /docs)
```

---

## Alternative: Direct upload/delete via API (without git)

> **Personal Access Token** (classic) banayein (scope: `repo`). `Settings → Developer settings → Personal access tokens`

**Upload/Replace:**
```bash
python scripts/manage_github_image.py upload <owner> <repo> <TOKEN> /path/to/your-photo.jpg
# Example:
# python scripts/manage_github_image.py upload radheshyam-meghwal my-photo-host ghp_xxx ./my.jpg
```

**Delete:**
```bash
python scripts/manage_github_image.py delete <owner> <repo> <TOKEN>
```

---

## Troubleshooting

- **404 on page**: Pages enable nahi hua ya branch/folder galat. Ensure: *Deploy from a branch* → `main` + `/docs`.
- **Photo not updating**: Browser cache. Hard refresh karein. Page JS me `?t=` cache-bust already added.
- **Branch `master` hai**: Scripts `main` assume karte hain. Branch rename karein ya script me last arg me branch pass karein.
- **Private repo**: GitHub Pages public content ke liye hota hai. Private repo pe Pages serve karne ke liye visibility Public karein (project site).

— Generated 2025-08-16 08:57 
