# Weebhook - WhatsApp Business API Webhook Server

A **FastAPI** webhook server designed to handle WhatsApp Business API callbacks and integrate with n8n for automation workflows.

## 🚀 Features

- **FastAPI Framework**: Modern, fast Python web framework
- **Webhook Verification**: Handles Meta's webhook verification process
- **Message Processing**: Receives and processes WhatsApp messages and status updates
- **Event Logging**: Stores webhook events for debugging and monitoring
- **Health Monitoring**: Built-in health check endpoints
- **n8n Integration Ready**: Designed to work seamlessly with n8n automation
- **Auto-generated API Docs**: Swagger UI documentation at `/docs`
- **Cloud Ready**: Optimized for Render deployment

## 📋 Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **GitHub account** (for deployment)
- **Render account** (free hosting)
- Meta Developer Account
- WhatsApp Business API access

## 🛠️ Installation

### Local Development
1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # Copy environment template
   copy env.example .env
   
   # Edit .env with your configuration
   VERIFY_TOKEN=your_custom_verify_token_here
   ```

4. **Run locally:**
   ```bash
   python main.py
   ```

## 🚀 Deployment to Render (Recommended)

### Quick Deploy with render.yaml
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add FastAPI webhook server"
   git push origin master
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Click "Apply"

3. **Get your public URL:**
   ```
   https://your-app-name.onrender.com
   ```

### Manual Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed manual setup instructions.

## 📱 Meta/WhatsApp Business API Configuration

### 1. Get Your Webhook URL
- **Local Development**: `http://localhost:3000/webhook`
- **Production**: `https://your-app-name.onrender.com/webhook`

### 2. Configure in Meta Developer Console
1. Go to [Meta Developers](https://developers.facebook.com/)
2. Navigate to your app → WhatsApp → Configuration
3. Set the following values:
   - **Webhook URL**: Your Render URL + `/webhook`
   - **Verify Token**: The same value you set in your environment variables

### 3. Subscribe to Webhook Fields
Make sure to subscribe to:
- `messages` - for incoming messages
- `message_statuses` - for delivery status updates

## 🔗 n8n Integration

### Option 1: Direct Webhook
Use the webhook URL directly in n8n:
```
https://your-app-name.onrender.com/webhook
```

### Option 2: Automatic Forwarding
Set the `N8N_WEBHOOK_URL` environment variable in Render:
```env
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
```

The server automatically forwards events to n8n when configured.

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with server information |
| `/webhook` | GET | Webhook verification (Meta calls this) |
| `/webhook` | POST | Receives webhook events from Meta |
| `/health` | GET | Health check endpoint |
| `/events` | GET | View recent webhook events |
| `/events` | DELETE | Clear webhook events log |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## 🌐 Deployment Options

### Render (Recommended)
- ✅ **Free hosting**
- ✅ **Auto-deploy** on GitHub push
- ✅ **HTTPS included**
- ✅ **Professional setup**

### Local Development
- ✅ **Fast development**
- ✅ **No internet required**
- ❌ **Not accessible from internet**

### Other Cloud Platforms
- **Railway**: Similar to Render
- **Vercel**: Great for Python apps
- **Heroku**: Classic option
- **PythonAnywhere**: Python-focused

## 🔒 Security Considerations

- **Verify Token**: Use a strong, unique verify token
- **HTTPS**: Always use HTTPS in production (Render provides this)
- **Environment Variables**: Keep sensitive data in environment variables
- **Input Validation**: FastAPI provides built-in validation

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VERIFY_TOKEN` | Meta webhook verification token | `your_verify_token_here` |
| `N8N_WEBHOOK_URL` | n8n webhook URL for forwarding | - |
| `PORT` | Server port (Render sets this) | 3000 |

## 🐛 Troubleshooting

### Local Development Issues
- Check Python version: `python --version`
- Verify dependencies: `pip list`
- Check port availability

### Render Deployment Issues
- Check build logs in Render dashboard
- Verify `main.py` exists and is correct
- Check environment variables

### Webhook Issues
- Verify Meta configuration
- Check webhook verification
- Review Render service logs

## 🐍 FastAPI Advantages

- **Performance**: Much faster than Flask
- **Type Safety**: Built-in type hints and validation
- **Documentation**: Auto-generated Swagger UI
- **Modern**: Latest Python features
- **Scalable**: Production-ready architecture

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Render Documentation](https://render.com/docs)
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta Webhooks Documentation](https://developers.facebook.com/docs/graph-api/webhooks)
- [n8n Documentation](https://docs.n8n.io/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - see LICENSE file for details. 