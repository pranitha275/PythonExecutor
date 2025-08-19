# 🚀 Deploy to Railway (Free - No Billing Required)

## **Step 1: Sign Up for Railway**
1. Go to [Railway.app](https://railway.app/)
2. Click **"Start a New Project"**
3. Sign up with your **GitHub account** (free)

## **Step 2: Create New Project**
1. Click **"Deploy from GitHub repo"**
2. Select your repository or **"Connect a GitHub repo"**
3. Choose the repository containing this code

## **Step 3: Configure Deployment**
1. **Project Name**: `python-executor` (or any name you prefer)
2. **Branch**: `main` (or your default branch)
3. Railway will automatically detect it's a Docker project

## **Step 4: Deploy**
1. Click **"Deploy Now"**
2. Wait for the build to complete (usually 2-3 minutes)
3. Railway will give you a **public URL** automatically

## **Step 5: Test Your Service**
Once deployed, you'll get a URL like: `https://your-app-name.railway.app`

Test it with:
```bash
curl -X POST https://YOUR_RAILWAY_URL/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello from Railway!\", \"status\": \"deployed\"}"}'
```

## **✅ What You Get**
- **Free hosting** (no billing required)
- **Public URL** accessible from anywhere
- **Automatic HTTPS**
- **Auto-deploy** when you push to GitHub
- **Monitoring and logs**

## **🔧 Railway Configuration**
The `railway.json` file tells Railway:
- Use your Dockerfile for building
- Run with gunicorn
- Use `/health` endpoint for health checks
- Restart on failures

## **📱 Railway Dashboard**
After deployment, you can:
- View logs in real-time
- Monitor performance
- Set environment variables
- Scale your service
- View metrics

## **🎯 Benefits of Railway**
- **No credit card required**
- **Generous free tier**
- **Very easy to use**
- **Professional hosting**
- **Great for demos and portfolios**

## **🚨 Important Notes**
- **Free tier limits**: Check Railway's current free tier limits
- **Auto-sleep**: Free tier may sleep after inactivity
- **Custom domains**: Available on paid plans

## **🔗 Next Steps**
1. Deploy to Railway using these steps
2. Test your service with the provided examples
3. Share the Railway URL for evaluation
4. Your Python Code Execution Service will be live on the internet!

---

**Need help?** Railway has excellent documentation and support. The deployment should be straightforward with these steps! 