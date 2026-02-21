import hashlib
import time
from typing import Optional

class LegalCheckpoint:
    \"\"\"
    Sistema de verificación legal inmutable para KemicalGrass.BOT.
    Garantiza que ningún usuario opere sin aceptación explícita.
    \"\"\"
    
    VERSION = \"2024.1-GLOBAL\"
    
    LEGAL_TEXTS = {
        'es': \"\"\"
⚠️ **DESCARGO LEGAL OBLIGATORIO** ⚠️

Al utilizar este bot, usted reconoce y acepta que:
1. **Neutralidad Tecnológica:** Esta plataforma es un proveedor de servicios tecnológicos (SaaS). No somos vendedores ni distribuidores de productos.
2. **Cumplimiento Local:** Usted es el único responsable de cumplir con las leyes de su jurisdicción con respecto al cannabis.
3. **Edad Mínima:** Declara ser mayor de edad legal en su país.
4. **Trazabilidad:** Su aceptación será registrada de forma inmutable para fines de cumplimiento normativo.

¿Acepta estos términos para continuar?
        \"\"\",
        'en': \"\"\"
⚠️ **MANDATORY LEGAL DISCLAIMER** ⚠️

By using this bot, you acknowledge and agree that:
1. **Technological Neutrality:** This platform is a technology service provider (SaaS). We are not sellers or distributors.
2. **Local Compliance:** You are solely responsible for complying with your local laws regarding cannabis.
3. **Minimum Age:** You declare you are of legal adult age in your country.
4. **Traceability:** Your acceptance will be immutably recorded for regulatory compliance purposes.

Do you accept these terms to continue?
        \"\"\"
    }

    def __init__(self, db_service):
        self.db = db_service

    async def requires_acceptance(self, user_id: int, tenant_id: int) -> bool:
        \"\"\"Verifica si el usuario necesita aceptar los términos.\"\"\"
        acceptance = await self.db.fetch_one(
            \"SELECT id FROM legal_acceptances WHERE user_id = $1 AND tenant_id = $2 AND terms_version = $3\",
            user_id, tenant_id, self.VERSION
        )
        return acceptance is None

    async def record_acceptance(self, user_id: int, tenant_id: int, user_data: str):
        \"\"\"Registra la aceptación con un hash inmutable.\"\"\"
        timestamp = str(time.time())
        acceptance_string = f\"{user_id}:{tenant_id}:{self.VERSION}:{timestamp}\"
        acceptance_hash = hashlib.sha256(acceptance_string.encode()).hexdigest()
        
        await self.db.execute(
            \"INSERT INTO legal_acceptances (user_id, tenant_id, terms_version, acceptance_hash) VALUES ($1, $2, $3, $4)\",
            user_id, tenant_id, self.VERSION, acceptance_hash
        )
        return acceptance_hash

    def get_legal_text(self, lang: str = 'es') -> str:
        return self.LEGAL_TEXTS.get(lang, self.LEGAL_TEXTS['es'])
