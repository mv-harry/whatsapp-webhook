# 🚀 Render Deployment Guide

## 📋 Prerequisites
- GitHub account
- Render account (free)

## 🎯 Step-by-Step Deployment

### 1. Push to GitHub
```bash
# Add all files
git add .

# Commit changes
git commit -m "Add FastAPI webhook server for Render deployment"

# Push to GitHub
git push origin master
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Click "Apply" to deploy

#### Option B: Manual Setup
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `weebhook-webhook`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `VERIFY_TOKEN`: Your custom verify token
   - `N8N_WEBHOOK_URL`: Your n8n webhook URL (optional)
7. Click "Create Web Service"

### 3. Get Your Public URL
After deployment, Render will give you:
```
https://your-app-name.onrender.com
```

### 4. Configure in Meta Developer Console
- **Callback URL**: `https://your-app-name.onrender.com/webhook`
- **Verify Token**: Same as your `VERIFY_TOKEN`

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VERIFY_TOKEN` | Meta webhook verification token | ✅ Yes |
| `N8N_WEBHOOK_URL` | n8n webhook URL for forwarding | ❌ No |

## 📱 Testing Your Webhook

### Test Endpoints:
- **Home**: `https://your-app.onrender.com/`
- **Health**: `https://your-app.onrender.com/health`
- **Events**: `https://your-app.onrender.com/events`
- **API Docs**: `https://your-app.onrender.com/docs`

### Test Webhook Verification:
```
GET https://your-app.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test123
```

## 🚨 Important Notes

- **Free tier**: 750 hours/month (about 31 days)
- **Auto-sleep**: Free services sleep after 15 minutes of inactivity
- **Wake-up time**: ~30 seconds when first request comes in
- **HTTPS**: Automatically provided by Render

## 🔍 Troubleshooting

### Build Fails:
- Check `requirements.txt` syntax
- Verify Python version compatibility

### Service Won't Start:
- Check start command in render.yaml
- Verify main.py exists and is correct

### Webhook Not Working:
- Check environment variables
- Verify Meta configuration
- Check Render service logs

## 🎉 Success!
Your webhook server is now:
- ✅ **Publicly accessible** from anywhere
- ✅ **Always online** (with free tier limitations)
- ✅ **HTTPS secured**
- ✅ **Auto-deploying** on GitHub push
- ✅ **Professional hosting**

## 📚 Additional Resources
- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp) 