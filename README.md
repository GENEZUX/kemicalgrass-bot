# KemicalGrass.BOT 🌿🤖

## "El Shopify de Telegram para el Cannabis Legal"

Plataforma SaaS multi-tenant diseñada para el comercio legal de productos de cannabis, con un enfoque integral en cumplimiento normativo, geobloqueo y trazabilidad.

### 🛡️ Filosofía Legal: "Somos Tecnología, No Vendedores"
La plataforma opera bajo un modelo de neutralidad tecnológica, donde cada tienda (tenant) es responsable de su operación, mientras el sistema garantiza que se cumplan los pasos de verificación legal obligatorios.

### 🚀 Características Principales
- **Arquitectura Multi-tenant:** Una sola instancia sirve a múltiples tiendas independientes.
- **Legal Checkpoint Mandatory:** Sistema de aceptación de términos inmutable y auditable antes de cualquier interacción.
- **Geoblocking Inteligente:** Restricción de acceso basada en la ubicación del usuario para cumplir con leyes locales.
- **Gestión de Inventario y Pedidos:** Flujo completo de eCommerce optimizado para Telegram.
- **Integración con Stripe:** Pagos seguros y cumplimiento de políticas de procesadores de pago.

### 📁 Estructura del Proyecto
- `src/core/`: Lógica central, seguridad y checkpoints legales.
- `src/models/`: Definiciones de base de datos (PostgreSQL).
- `src/handlers/`: Controladores de comandos de Telegram (python-telegram-bot v20+).
- `src/services/`: Integraciones externas (Stripe, Geolocation).
- `migrations/`: Esquemas de base de datos y evoluciones.

### 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **Framework:** python-telegram-bot
- **Base de Datos:** PostgreSQL
- **Caché/Sesiones:** Redis
- **Infraestructura:** Docker / Vercel / Railway

---
© 2024 Barbosa Agency Pro - Tecnología para el Futuro Legal.
