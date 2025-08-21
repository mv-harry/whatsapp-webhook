# Weebhook - WhatsApp Business API Webhook Server

A **Python Flask** webhook server designed to handle WhatsApp Business API callbacks and integrate with n8n for automation workflows.

## 🚀 Features

- **Webhook Verification**: Handles Meta's webhook verification process
- **Message Processing**: Receives and processes WhatsApp messages and status updates
- **Event Logging**: Stores webhook events for debugging and monitoring
- **Health Monitoring**: Built-in health check endpoints
- **n8n Integration Ready**: Designed to work seamlessly with n8n automation
- **Python Flask**: Modern, lightweight web framework

## 📋 Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- Meta Developer Account
- WhatsApp Business API access

## 🛠️ Installation

### Option 1: Using requirements.txt
1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Using setup.py
```bash
python setup.py install
```

### Option 3: Using pip directly
```bash
pip install Flask Flask-CORS python-dotenv requests gunicorn
```

3. **Configure environment variables:**
   ```bash
   # On Windows
   copy env.example .env
   
   # On Linux/Mac
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   PORT=3000
   VERIFY_TOKEN=your_custom_verify_token_here
   ```

## 🚀 Usage

### Development Mode
```bash
python server.py
```

### Production Mode (using Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:3000 server:app
```

### Using the setup script (Windows)
```bash
setup.bat
```

The server will start on port 3000 (or the port specified in your .env file).

## 📱 Meta/WhatsApp Business API Configuration

### 1. Get Your Webhook URL
- **Local Development**: Use ngrok to expose your local server
- **Production**: Use your actual domain

### 2. Configure in Meta Developer Console
1. Go to [Meta Developers](https://developers.facebook.com/)
2. Navigate to your app → WhatsApp → Configuration
3. Set the following values:
   - **Webhook URL**: `https://your-domain.com/webhook`
   - **Verify Token**: The same value you set in your `.env` file

### 3. Subscribe to Webhook Fields
Make sure to subscribe to:
- `messages` - for incoming messages
- `message_statuses` - for delivery status updates

## 🔗 n8n Integration

### Option 1: Direct Webhook
Use the webhook URL directly in n8n:
```
https://your-domain.com/webhook
```

### Option 2: Automatic Forwarding
The server automatically forwards events to n8n if you set the `N8N_WEBHOOK_URL` environment variable:

```env
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with server information |
| `/webhook` | GET | Webhook verification (Meta calls this) |
| `/webhook` | POST | Receives webhook events from Meta |
| `/health` | GET | Health check endpoint |
| `/events` | GET | View recent webhook events |
| `/events` | DELETE | Clear webhook events log |

## 🌐 Exposing Your Local Server

### Using ngrok (Recommended for development)
```bash
# Install ngrok
# Download from: https://ngrok.com/download

# Expose your local server
ngrok http 3000
```

### Using pyngrok (Python package)
```bash
# Install pyngrok
pip install pyngrok

# In Python
from pyngrok import ngrok
url = ngrok.connect(3000)
print(url)
```

### Using localtunnel
```bash
# Install localtunnel
npm install -g localtunnel

# Expose your local server
lt --port 3000
```

## 🔒 Security Considerations

- **Verify Token**: Use a strong, unique verify token
- **HTTPS**: Always use HTTPS in production
- **Rate Limiting**: Consider implementing rate limiting for production use
- **Input Validation**: The server includes basic validation but consider additional security measures

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3000 |
| `VERIFY_TOKEN` | Meta webhook verification token | `your_verify_token_here` |
| `META_APP_ID` | Your Meta App ID | - |
| `META_APP_SECRET` | Your Meta App Secret | - |
| `META_ACCESS_TOKEN` | Your Meta Access Token | - |
| `N8N_WEBHOOK_URL` | n8n webhook URL for forwarding | - |

## 🐛 Troubleshooting

### Webhook Verification Fails
- Check that your verify token matches exactly
- Ensure the webhook URL is accessible from the internet
- Check server logs for detailed error messages

### No Webhook Events Received
- Verify webhook subscription in Meta Developer Console
- Check that your server is accessible from the internet
- Ensure proper webhook field subscriptions

### Server Won't Start
- Check if port 3000 is already in use
- Verify all dependencies are installed: `pip list`
- Check for syntax errors in configuration files
- Ensure Python 3.8+ is installed: `python --version`

### Import Errors
- Make sure all requirements are installed: `pip install -r requirements.txt`
- Check Python path and virtual environment

## 🐍 Python-Specific Notes

- **Virtual Environment**: Consider using a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Linux/Mac
  venv\Scripts\activate     # On Windows
  ```

- **Dependencies**: All dependencies are listed in `requirements.txt`
- **Flask Debug**: Debug mode is enabled by default for development
- **Gunicorn**: Use Gunicorn for production deployment

## 📚 Additional Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta Webhooks Documentation](https://developers.facebook.com/docs/graph-api/webhooks)
- [n8n Documentation](https://docs.n8n.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - see LICENSE file for details. 