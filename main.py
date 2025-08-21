from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import json
from datetime import datetime
import requests

app = FastAPI(
    title="Weebhook - WhatsApp Business API Webhook Server",
    description="FastAPI webhook server for WhatsApp Business API integration",
    version="1.0.0"
)

# Configuration
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'your_verify_token_here')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Store webhook events
webhook_events = []

@app.get("/")
async def home():
    return {
        "service": "Weebhook - WhatsApp Business API Webhook Server",
        "version": "1.0.0",
        "language": "FastAPI",
        "status": "running",
        "deployed_on": "Render",
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health",
            "events": "/events",
            "docs": "/docs"
        }
    }

@app.get("/webhook")
async def verify_webhook(mode: str = None, token: str = None, challenge: str = None):
    """WhatsApp Business API Webhook Verification"""
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('✅ Webhook verified successfully!')
            return challenge
        else:
            print('❌ Webhook verification failed')
            raise HTTPException(status_code=403, detail="Forbidden")
    else:
        print('❌ Missing mode or token parameters')
        raise HTTPException(status_code=400, detail="Bad Request")

@app.post("/webhook")
async def webhook_callback(request: Request):
    """WhatsApp Business API Webhook Callback"""
    try:
        body = await request.json()
        print('📨 Webhook received:', json.dumps(body, indent=2))
        
        # Check if this is a WhatsApp Business API webhook
        if body.get('object') == 'whatsapp_business_account':
            # Process each entry
            for entry in body.get('entry', []):
                # Process each change
                for change in entry.get('changes', []):
                    if change.get('field') == 'messages':
                        # Process messages
                        for message in change.get('value', {}).get('messages', []):
                            print('💬 New message received:', {
                                'from': message.get('from'),
                                'timestamp': message.get('timestamp'),
                                'type': message.get('type'),
                                'messageId': message.get('id')
                            })
                            
                            # Store webhook event for debugging
                            webhook_events.append({
                                'timestamp': datetime.now().isoformat(),
                                'type': 'message',
                                'data': message
                            })
                            
                            # Forward to n8n if configured
                            if N8N_WEBHOOK_URL:
                                try:
                                    response = requests.post(
                                        N8N_WEBHOOK_URL,
                                        json=message,
                                        headers={'Content-Type': 'application/json'},
                                        timeout=10
                                    )
                                    print(f'📤 Forwarded to n8n: {response.status_code}')
                                except Exception as e:
                                    print(f'❌ Failed to forward to n8n: {e}')
                    
                    elif change.get('field') == 'message_statuses':
                        # Process message status updates
                        for status in change.get('value', {}).get('statuses', []):
                            print('📊 Message status update:', {
                                'messageId': status.get('id'),
                                'status': status.get('status'),
                                'timestamp': status.get('timestamp')
                            })
                            
                            webhook_events.append({
                                'timestamp': datetime.now().isoformat(),
                                'type': 'status_update',
                                'data': status
                            })
            
            return {"status": "OK"}
        else:
            print(f'⚠️ Received webhook for different object: {body.get("object")}')
            return {"status": "OK"}
            
    except Exception as error:
        print('❌ Error processing webhook:', error)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "service": "WhatsApp Business API Webhook Server",
        "language": "FastAPI"
    }

@app.get("/events")
async def get_events():
    """Webhook events log endpoint (for debugging)"""
    return {
        "totalEvents": len(webhook_events),
        "events": webhook_events[-50:]  # Last 50 events
    }

@app.delete("/events")
async def clear_events():
    """Clear events endpoint (for debugging)"""
    global webhook_events
    webhook_events = []
    return {"message": "Events cleared successfully"}

if __name__ == "__main__":
    print('🚀 Starting FastAPI Weebhook Webhook Server...')
    print('📋 Webhook URL: http://localhost:8000/webhook')
    print('🔍 Health check: http://localhost:8000/health')
    print('📊 Events log: http://localhost:8000/events')
    print('📚 API Documentation: http://localhost:8000/docs')
    print('\n📱 To configure in Meta/WhatsApp Business API:')
    print(f'   Callback URL: http://localhost:8000/webhook')
    print(f'   Verify Token: {VERIFY_TOKEN}')
    print('\n💡 For production, deploy to Render for public access')
    print('⚡ FastAPI webhook server ready!')
    
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000))) 