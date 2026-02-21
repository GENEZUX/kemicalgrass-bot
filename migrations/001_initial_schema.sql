-- KEMICALGRASS.BOT - Initial Schema
-- Multi-tenant eCommerce for Legal Cannabis

CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    telegram_token VARCHAR(255) UNIQUE NOT NULL,
    stripe_api_key VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY, -- Telegram User ID
    tenant_id INTEGER REFERENCES tenants(id),
    username VARCHAR(255),
    full_name VARCHAR(255),
    language_code VARCHAR(10),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE legal_acceptances (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    tenant_id INTEGER REFERENCES tenants(id),
    terms_version VARCHAR(50) NOT NULL,
    acceptance_hash VARCHAR(64) NOT NULL,
    accepted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address_hash VARCHAR(64)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price_cents INTEGER NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    category VARCHAR(100),
    is_legal_regulated BOOLEAN DEFAULT TRUE,
    image_url TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    tenant_id INTEGER REFERENCES tenants(id),
    status VARCHAR(50) DEFAULT 'pending', -- pending, paid, shipped, cancelled
    total_amount_cents INTEGER NOT NULL,
    payment_intent_id VARCHAR(255),
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE geoblocking_rules (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    country_code VARCHAR(2) NOT NULL,
    is_allowed BOOLEAN DEFAULT TRUE,
    restricted_categories TEXT[]
);
