import openai
import os
import re
from pdf_generator import QuotePDF
from contabilium_client import ContabiliumClient
from whatsapp_sender import send_message, send_document

class HarryAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.contabilium = ContabiliumClient()
        self.pdf_gen = QuotePDF()
        openai.api_key = self.openai_api_key

    async def process_message(self, text: str, sender: str, group: str = None):
        """Procesa un mensaje y decide qué hacer"""
        is_private = group is None

        # Si es privado, avisar a Martín
        if is_private:
            await self.notify_martin(sender, text[:100])

        # Clasificar intención con OpenAI
        intent = await self.classify_intent(text)

        if intent == "cotizacion":
            return await self.handle_quote(text, sender, group)
        elif intent == "descuento":
            return await self.handle_discount(text, sender, group)
        elif intent == "seguimiento":
            return await self.handle_tracking(text, sender, group)
        else:
            return "No entendí bien. ¿Podés reformular?", None

    async def classify_intent(self, text):
        """Usa GPT para entender qué quiere el usuario"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Clasificá el mensaje en una de estas categorías: cotizacion, descuento, seguimiento, otro. Respondé solo la palabra."},
                    {"role": "user", "content": text}
                ],
                temperature=0,
                max_tokens=10
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error clasificando intent: {e}")
            return "otro"

    async def handle_quote(self, text, sender, group):
        """Lógica de cotización"""
        # Extraer datos básicos con regex (simplificado)
        # Buscar cantidad y producto
        match = re.search(r'(\d+)\s*(\w+)', text)
        if match:
            cantidad = match.group(1)
            producto = match.group(2)
        else:
            return "Por favor, indicá cantidad y producto (ej: 10 onus)", None

        # Buscar cliente (después de "para")
        match_cliente = re.search(r'para\s+([A-Za-z0-9\s]+)', text)
        cliente = match_cliente.group(1).strip() if match_cliente else "Cliente no especificado"

        # Simular consulta a Contabilium (luego se conecta real)
        precio_unitario = 100  # Esto debería venir de Contabilium
        total = int(cantidad) * precio_unitario

        # Generar PDF
        pdf_data = {
            "id": "COT-001",
            "cliente": cliente,
            "cuit": "30-12345678-9",  # Placeholder
            "items": [
                {"sku": producto, "descripcion": f"Producto {producto}", "cantidad": cantidad, "precio_unitario": precio_unitario, "total": total}
            ],
            "subtotal": total,
            "iva": total * 0.21,
            "total": total * 1.21,
            "pago": "Transferencia",
            "validez": "2026-03-22"
        }
        pdf_path = self.pdf_gen.generate(pdf_data)

        frase = f"Listo @{sender}. Te envío la cotización."
        return frase, pdf_path

    async def handle_discount(self, text, sender, group):
        """Lógica de descuentos"""
        match = re.search(r'(\d+)%', text)
        if not match:
            return f"@{sender} ¿Qué porcentaje de descuento querés aplicar?", None
        discount = int(match.group(1))

        if discount <= 5:
            return f"Hecho @{sender}. Aplicado {discount}%. Adjunto PDF.", None
        elif discount < 10:
            await self.request_approval(sender, discount, text)
            return f"@{sender} Consulto con Martín y te confirmo.", None
        else:
            return f"@{sender} Ese % no me cierra. ¿Vemos contado o más unidades?", None

    async def handle_tracking(self, text, sender, group):
        # Placeholder
        return f"@{sender} El pedido está en preparación.", None

    async def notify_martin(self, sender, summary):
        """Envía un WhatsApp a Martín avisando del chat privado"""
        martin_phone = os.getenv("MARTIN_PHONE_NUMBER")
        if martin_phone:
            msg = f"🔔 Chat privado de {sender}: {summary}"
            await send_message(martin_phone, msg)

    async def request_approval(self, sender, discount, text):
        """Pide aprobación a Martín"""
        martin_phone = os.getenv("MARTIN_PHONE_NUMBER")
        if martin_phone:
            msg = f"⚠️ Solicitud de aprobación de {sender}: {discount}% de descuento. Mensaje: {text}"
            await send_message(martin_phone, msg)
