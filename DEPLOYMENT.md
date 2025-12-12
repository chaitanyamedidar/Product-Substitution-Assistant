# Deployment Guide

## Prerequisites

1. **GitHub Account**: Create one at https://github.com if you don't have one
2. **Streamlit Cloud Account**: Sign up at https://streamlit.io/cloud (use your GitHub account)

## Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `product-substitution-assistant` (or any name you prefer)
3. Description: "Knowledge Graph-based product substitution system using classical AI"
4. Set to **Public** (required for free Streamlit deployment)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Push Code to GitHub

Open PowerShell in the project directory (`d:\Webdev\Assignment`) and run:

```powershell
# Initialize Git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Product Substitution Assistant"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/product-substitution-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your repository: `YOUR_USERNAME/product-substitution-assistant`
4. Branch: `main`
5. Main file path: `app.py`
6. Click "Deploy!"

The deployment will take 2-3 minutes. Once complete, you'll get a public URL like:
```
https://YOUR_USERNAME-product-substitution-assistant-app-xxxxx.streamlit.app
```

### Step 4: Update README

Once deployed, update the README.md file with your live app URL:

1. Edit `README.md`
2. Find the line: `**Deployed App:** [Will be added after deployment]`
3. Replace with: `**Deployed App:** [Live Demo](YOUR_STREAMLIT_URL)`
4. Commit and push:
   ```powershell
   git add README.md
   git commit -m "Add deployed app URL"
   git push
   ```

## Troubleshooting

### Issue: Git not installed
**Solution**: Download from https://git-scm.com/download/win

### Issue: Git authentication failed
**Solution**: Use a Personal Access Token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Issue: Streamlit app crashes on deployment
**Solution**: Check the logs in Streamlit Cloud dashboard
- Common issues:
  - Missing `products.json` file (ensure it's committed)
  - Wrong file paths (use relative paths)
  - Dependencies not installed (check `requirements.txt`)

### Issue: App loads but shows errors
**Solution**: 
1. Check that `products.json` is in the same directory as `app.py`
2. Verify all Python files are committed
3. Check Streamlit Cloud logs for specific errors

## Verification Checklist

After deployment, verify:

- [ ] App loads without errors
- [ ] Product dropdown shows all 50 products
- [ ] Selecting an in-stock product shows exact match
- [ ] Selecting an out-of-stock product shows alternatives
- [ ] Filters work (price, tags, brand)
- [ ] Explanations are displayed correctly
- [ ] Sidebar shows system stats

## Final Deliverables

Submit these two links:

1. **GitHub Repository**: `https://github.com/YOUR_USERNAME/product-substitution-assistant`
2. **Deployed App**: `https://YOUR_USERNAME-product-substitution-assistant-app-xxxxx.streamlit.app`

## Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all files are committed to GitHub
3. Ensure repository is public
4. Check that `requirements.txt` has correct dependencies

---

**Good luck with your deployment!** 🚀
