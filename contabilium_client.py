import httpx
import os

class ContabiliumClient:
    def __init__(self):
        self.api_key = os.getenv("CONTABILIUM_API_KEY")
        self.base_url = os.getenv("CONTABILIUM_URL")

    async def get_product_info(self, sku: str) -> dict:
        """Obtiene producto desde Contabilium"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/products",
                params={"sku": sku},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()

    # Agrega más métodos según necesites
