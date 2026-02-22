import httpx
import os

PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

async def send_message(to: str, text: str):
    """Envía un mensaje de texto por WhatsApp"""
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()

async def upload_media(file_path: str) -> str:
    """Sube un archivo a los servidores de Meta y devuelve el media_id"""
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/pdf')
    }
    data = {
        "messaging_product": "whatsapp"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data, files=files)
        return response.json().get("id")

async def send_document(to: str, file_path: str):
    """Envía un documento PDF por WhatsApp"""
    media_id = await upload_media(file_path)
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": "cotizacion.pdf",
            "caption": "Cotización adjunta"
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()
