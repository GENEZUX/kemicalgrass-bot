import httpx
from typing import List, Optional

class GeoblockingService:
    \"\"\"
    Servicio de georestricción para KemicalGrass.BOT.
    Verifica si un usuario puede acceder basándose en su ubicación.
    \"\"\"
    
    def __init__(self, db_service):
        self.db = db_service
        self.api_url = \"http://ip-api.com/json/\"

    async def get_user_country(self, ip_address: str) -> Optional[str]:
        \"\"\"Obtiene el código de país (ISO 3166-1 alpha-2) de una IP.\"\"\"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f\"{self.api_url}{ip_address}\")
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('countryCode')
        except Exception as e:
            print(f\"Error en geolocalización: {e}\")
        return None

    async def is_allowed(self, tenant_id: int, country_code: str) -> bool:
        \"\"\"Verifica si el país está permitido para el tenant específico.\"\"\"
        rule = await self.db.fetch_one(
            \"SELECT is_allowed FROM geoblocking_rules WHERE tenant_id = $1 AND country_code = $2\",
            tenant_id, country_code
        )
        # Si no hay regla específica, por defecto permitimos (o restringimos según política del SaaS)
        if rule is None:
            return True
        return rule['is_allowed']

    async def check_access(self, tenant_id: int, ip_address: str) -> bool:
        \"\"\"Flujo completo de validación de acceso.\"\"\"
        country = await self.get_user_country(ip_address)
        if not country:
            # Si no podemos determinar el país, podemos ser conservadores y denegar
            return False
        return await self.is_allowed(tenant_id, country)
