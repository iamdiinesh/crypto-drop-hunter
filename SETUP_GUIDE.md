# Crypto Drop Hunter - Setup Guide

**Your automated drop finder runs 3x daily (8am, 3pm, 12am UTC) and emails results to dineshgupt369@gmail.com**

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create a GitHub Repository

1. Go to **github.com** → Log in as **iamdiinesh**
2. Click **New Repository** (top right)
3. Name it: `crypto-drop-hunter`
4. Make it **Public** (GitHub Actions needs this for free tier)
5. Click **Create Repository**

---

### Step 2: Add Files to Your Repo

1. In your new repo, click **Add file** → **Create new file**
2. Name: `crypto_drop_hunter.py`
3. Copy the contents from the Python script file
4. Click **Commit changes**

**Repeat for workflow file:**
1. Click **Add file** → **Create new file**
2. Path: `.github/workflows/drop_hunter.yml`
3. Copy the workflow YAML contents
4. Click **Commit changes**

*(GitHub will auto-create the .github/workflows folder)*

---

### Step 3: Set Up Email (Gmail)

Since we're using Gmail for automated emails:

1. **Enable 2-Step Verification** on your Google Account:
   - Go to **myaccount.google.com**
   - Left sidebar → **Security**
   - Scroll to "How you sign in to Google"
   - Enable **2-Step Verification** (if not already on)

2. **Generate App Password**:
   - Go back to **Security** page
   - Scroll to "App passwords" (only appears after 2FA is on)
   - Select **Mail** and **Windows Computer** (or device type)
   - Google generates a 16-character password
   - **Copy this password**

3. **Add to GitHub Secrets**:
   - In your repo, go to **Settings** (top right)
   - Left sidebar → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   
   **Add two secrets:**
   
   **Secret 1:**
   - Name: `SENDER_EMAIL`
   - Value: `dineshgupt369@gmail.com`
   - Click **Add secret**
   
   **Secret 2:**
   - Name: `APP_PASSWORD`
   - Value: (paste the 16-char password from Google)
   - Click **Add secret**

---

### Step 4: Verify It's Running

1. In your repo, click **Actions** tab (top)
2. You should see "Crypto Drop Hunter - 3x Daily" workflow
3. Wait for the next scheduled time (8am, 3pm, or 12am UTC) OR manually trigger:
   - Click the workflow name
   - Click **Run workflow** → **Run workflow** button

4. Check **Actions** tab for "drop-hunter" job
   - Green ✓ = Success
   - Red ✗ = Check logs (click the job to see error)

---

### Step 5: Receive Email Results

Once the workflow runs successfully:
- Check **dineshgupt369@gmail.com** inbox
- You'll get an email with all active drops
- Each email shows: Project name, Chain, Type, Status, Gas estimate

---

## 📊 What the Script Does

**Scrapes from:**
- ✅ Airdrop Alert
- ✅ DeFi Pulse  
- ✅ Solana Drops
- ✅ OpenSea Drops

**Filters for:**
- ✅ Solana, Ethereum, Polygon, Arbitrum
- ✅ Gas < $3 OR Free
- ✅ Both NFT and Token airdrops

**Removes:**
- Duplicates
- Old/closed drops
- High gas fees

---

## ⏰ Schedule Details

The script runs at:
- **8:00 AM UTC** (adjust for your timezone)
- **3:00 PM UTC**
- **12:00 AM UTC** (midnight)

**Want different times?** Edit `.github/workflows/drop_hunter.yml`:
```yaml
  - cron: '0 8 * * *'     # Change 8 to desired hour (0-23)
```

---

## 🔧 Customization

### Change Target Chains
Edit `crypto_drop_hunter.py`, line ~25:
```python
CHAINS = ["solana", "ethereum", "polygon", "arbitrum"]
```
Remove or add chains as needed.

### Change Max Gas Price
Line ~26:
```python
MAX_GAS = 3  # Change to your preferred limit
```

### Change Email Recipient
Line ~24:
```python
TARGET_EMAIL = "dineshgupt369@gmail.com"  # Or another email
```

---

## 🛠️ Troubleshooting

**Script isn't running?**
- Check GitHub Actions status: Repo → Actions tab
- Click failed job to see error logs

**Not getting emails?**
- Check spam folder
- Verify App Password is correct (Settings → Secrets)
- Make sure Gmail 2FA is enabled

**Want to test now?**
- In GitHub Actions tab, click **Run workflow** manually
- Job runs immediately

---

## 📱 Next Steps (Optional)

**To improve drop quality:**
1. Add Discord webhook for real-time alerts
2. Add TVL/user thresholds to filter scams
3. Add Phantom wallet connection monitoring
4. Create a dashboard to view all drops

**Just let me know and I can enhance it!**

---

## ⚠️ Important Notes


✅ **Free:** GitHub Actions free tier = unlimited runs  
✅ **Automated:** Runs on schedule, no manual intervention  
✅ **Your data:** Results only in your email + GitHub artifacts (7-day retention)

---

**Questions? Ask me anytime.** Once this is live, you'll get drop alerts 3x daily automatically.
