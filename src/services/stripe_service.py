import stripe
from typing import Optional, Dict

class StripeService:
    \"\"\"
    Integración con Stripe para pagos en KemicalGrass.BOT.
    Soporta múltiples tenants con sus propias llaves API.
    \"\"\"
    
    def __init__(self, default_api_key: str):
        self.default_api_key = default_api_key
        stripe.api_key = default_api_key

    async def create_payment_intent(self, amount_cents: int, currency: str = \"usd\", metadata: Dict = None, tenant_api_key: str = None) -> Optional[Dict]:
        \"\"\"Crea un PaymentIntent de Stripe.\"\"\"
        try:
            api_key = tenant_api_key or self.default_api_key
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                api_key=api_key
            )
            return intent
        except Exception as e:
            print(f\"Error creando pago en Stripe: {e}\")
            return None

    async def verify_payment(self, payment_intent_id: str, tenant_api_key: str = None) -> bool:
        \"\"\"Verifica si un pago ha sido completado exitosamente.\"\"\"
        try:
            api_key = tenant_api_key or self.default_api_key
            intent = stripe.PaymentIntent.retrieve(payment_intent_id, api_key=api_key)
            return intent.status == \"succeeded\"
        except Exception as e:
            print(f\"Error verificando pago: {e}\")
            return False
