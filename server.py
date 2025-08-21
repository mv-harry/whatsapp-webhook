from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', 3000))
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'your_verify_token_here')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Store webhook events for debugging/logging
webhook_events = []

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """WhatsApp Business API Webhook Verification"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('✅ Webhook verified successfully!')
            return challenge, 200
        else:
            print('❌ Webhook verification failed')
            return 'Forbidden', 403
    else:
        print('❌ Missing mode or token parameters')
        return 'Bad Request', 400

@app.route('/webhook', methods=['POST'])
def webhook_callback():
    """WhatsApp Business API Webhook Callback"""
    try:
        body = request.get_json()
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
            
            return 'OK', 200
        else:
            print(f'⚠️ Received webhook for different object: {body.get("object")}')
            return 'OK', 200
            
    except Exception as error:
        print('❌ Error processing webhook:', error)
        return 'Internal Server Error', 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'service': 'WhatsApp Business API Webhook Server',
        'language': 'Python'
    })

@app.route('/events', methods=['GET'])
def get_events():
    """Webhook events log endpoint (for debugging)"""
    return jsonify({
        'totalEvents': len(webhook_events),
        'events': webhook_events[-50:]  # Last 50 events
    })

@app.route('/events', methods=['DELETE'])
def clear_events():
    """Clear events endpoint (for debugging)"""
    global webhook_events
    webhook_events = []
    return jsonify({'message': 'Events cleared successfully'})

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with server information"""
    return jsonify({
        'service': 'Weebhook - WhatsApp Business API Webhook Server',
        'version': '1.0.0',
        'language': 'Python',
        'endpoints': {
            'webhook': '/webhook',
            'health': '/health',
            'events': '/events',
            'home': '/'
        },
        'status': 'running'
    })

if __name__ == '__main__':
    print('🚀 Starting Weebhook Webhook Server...')
    print(f'📋 Webhook URL: http://localhost:{PORT}/webhook')
    print(f'🔍 Health check: http://localhost:{PORT}/health')
    print(f'📊 Events log: http://localhost:{PORT}/events')
    print(f'🏠 Home: http://localhost:{PORT}/')
    print('\n📱 To configure in Meta/WhatsApp Business API:')
    print(f'   Callback URL: http://localhost:{PORT}/webhook')
    print(f'   Verify Token: {VERIFY_TOKEN}')
    print('\n💡 For production, use ngrok or similar to expose your local server')
    print('🐍 Python webhook server ready!')
    
    app.run(host='0.0.0.0', port=PORT, debug=True) 