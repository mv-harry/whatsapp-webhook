from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

class QuotePDF:
    def generate(self, quote_data: dict) -> str:
        """Genera PDF y devuelve ruta del archivo"""
        filename = f"/tmp/cotizacion_{quote_data['id']}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)

        # Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "IBRICOM S.A.S.")
        c.setFont("Helvetica", 10)
        c.drawString(50, 785, "CUIT: 30-12345678-9")
        c.drawString(50, 770, "Tel: (011) 1234-5678")

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 720, f"COTIZACIÓN #{quote_data['id']}")

        # Datos del cliente
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 690, "Cliente:")
        c.setFont("Helvetica", 11)
        c.drawString(50, 675, f"{quote_data['cliente']}")
        c.drawString(50, 660, f"CUIT: {quote_data['cuit']}")

        # Tabla de productos
        y = 620
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Código")
        c.drawString(150, y, "Descripción")
        c.drawString(350, y, "Cant.")
        c.drawString(400, y, "P.Unit.")
        c.drawString(480, y, "Total")

        y -= 20
        c.setFont("Helvetica", 10)
        for item in quote_data['items']:
            c.drawString(50, y, item['sku'])
            c.drawString(150, y, item['descripcion'][:30])
            c.drawString(350, y, str(item['cantidad']))
            c.drawString(400, y, f"${item['precio_unitario']:,.2f}")
            c.drawString(480, y, f"${item['total']:,.2f}")
            y -= 20

        # Totales
        y -= 30
        c.setFont("Helvetica-Bold", 11)
        c.drawString(400, y, "Subtotal:")
        c.drawString(480, y, f"${quote_data['subtotal']:,.2f}")
        y -= 15
        c.drawString(400, y, "IVA 21%:")
        c.drawString(480, y, f"${quote_data['iva']:,.2f}")
        y -= 15
        c.drawString(400, y, "TOTAL:")
        c.drawString(480, y, f"${quote_data['total']:,.2f}")

        # Condiciones
        y -= 50
        c.setFont("Helvetica", 9)
        c.drawString(50, y, f"Condición de pago: {quote_data['pago']}")
        y -= 15
        c.drawString(50, y, f"Válido hasta: {quote_data['validez']}")
        y -= 15
        c.drawString(50, y, "Los precios NO incluyen IVA. El IVA se factura por separado.")

        c.save()
        return filename
