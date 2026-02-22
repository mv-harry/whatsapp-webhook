from fastapi import FastAPI, Request
import os
import logging
from harry_agent import HarryAgent
from whatsapp_sender import send_message, send_document

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
agent = HarryAgent()

# Variables de entorno
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
MARTIN_PHONE = os.getenv("MARTIN_PHONE_NUMBER")

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verificación que hace Meta cuando configuras el webhook"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    logger.info(f"Verificación: mode={mode}, token={token}")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verificado correctamente")
        return int(challenge)
    logger.error("Verificación fallida")
    return {"error": "Verification failed"}, 403

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Aquí llegan los mensajes de WhatsApp"""
    data = await request.json()
    logger.info(f"Webhook recibido: {data}")
    
    try:
        # Verificar que sea un mensaje de WhatsApp
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        value = change.get("value", {})
                        messages = value.get("messages", [])
                        
                        for message in messages:
                            # Datos del mensaje
                            phone = message.get("from")  # Número del remitente
                            message_type = message.get("type")
                            
                            if message_type == "text":
                                text = message.get("text", {}).get("body", "")
                                logger.info(f"Mensaje de {phone}: {text}")
                                
                                # Determinar el grupo (simplificado: por ahora todos son grupo "Comercial")
                                group = "Comercial"  # Luego puedes mejorarlo
                                
                                # Procesar con Harry
                                respuesta, pdf_path = await agent.process_message(text, phone, group)
                                
                                # Enviar respuesta de texto
                                await send_message(phone, respuesta)
                                
                                # Si hay PDF, enviarlo
                                if pdf_path:
                                    await send_document(phone, pdf_path)
                            else:
                                logger.info(f"Mensaje no es texto: {message_type}")
    except Exception as e:
        logger.exception(f"Error procesando webhook: {e}")
    
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
