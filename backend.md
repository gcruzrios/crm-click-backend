# Bemantis CRM — Especificación Backend
**Versión 1.3 — Junio 2026**

---

## Stack técnico

| Componente | Tecnología |
|---|---|
| Framework | FastAPI (Python 3.11+) |
| Base de datos | PostgreSQL 15+ |
| ORM | SQLAlchemy 2.x (async) |
| Migraciones | Alembic |
| Autenticación | JWT (python-jose) + bcrypt |
| Validación | Pydantic v2 |
| Servidor | Uvicorn + Gunicorn |
| Hosting | Heroku (Heroku-24) |
| Variables de entorno | python-decouple o dotenv |

---

## Estructura de carpetas

```txt
backend/
├── app/
│   ├── main.py                    # Instancia FastAPI, CORS, routers
│   ├── core/
│   │   ├── config.py              # Settings desde .env
│   │   ├── security.py            # JWT, hashing
│   │   └── permissions.py         # Dependencias de rol
│   ├── db/
│   │   ├── session.py             # AsyncSession factory
│   │   └── base.py                # Base declarativa SQLAlchemy
│   ├── models/                    # Modelos SQLAlchemy (tablas)
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── contact.py
│   │   ├── lead.py
│   │   ├── opportunity.py
│   │   ├── service.py
│   │   ├── quote.py
│   │   ├── quote_item.py
│   │   ├── task.py
│   │   └── activity.py
│   ├── schemas/                   # Pydantic v2 schemas
│   │   ├── common.py              # PaginatedResponse, MessageResponse
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── contact.py
│   │   ├── lead.py
│   │   ├── opportunity.py
│   │   ├── service.py
│   │   ├── quote.py
│   │   ├── task.py
│   │   └── activity.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py          # Incluye todos los routers
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── clients.py
│   │       ├── contacts.py
│   │       ├── leads.py
│   │       ├── opportunities.py
│   │       ├── services.py
│   │       ├── quotes.py
│   │       ├── tasks.py
│   │       ├── activities.py
│   │       └── reports.py
│   ├── services/                  # Lógica de negocio desacoplada
│   │   ├── auth_service.py
│   │   ├── quote_calculator.py    # Cálculo servidor-side
│   │   ├── lead_converter.py      # Conversión lead → cliente/oportunidad
│   │   ├── activity_logger.py     # Auto-registro de actividades
│   │   └── report_service.py
│   └── utils/
│       ├── pagination.py
│       └── date_utils.py
├── alembic/
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── api/
├── requirements.txt
├── Procfile                       # web: gunicorn app.main:app ...
└── .env
```

---

## Entidades y esquema SQL

### Extensiones requeridas

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

### users

```sql
CREATE TABLE users (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name        VARCHAR(150) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    password_hash    TEXT NOT NULL,
    role             VARCHAR(30) NOT NULL DEFAULT 'sales',
    -- Valores: admin | manager | sales | viewer
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at    TIMESTAMP,                          -- [NUEVO] auditoría
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
```

> **Observación:** Agregar `last_login_at` es útil para auditoría y detección de cuentas inactivas.

---

### clients

```sql
CREATE TABLE clients (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(180) NOT NULL,
    client_type     VARCHAR(30) NOT NULL DEFAULT 'company',
    -- Valores: company | individual
    industry        VARCHAR(100),
    website         VARCHAR(255),
    phone           VARCHAR(50),
    email           VARCHAR(150),
    country         VARCHAR(100) DEFAULT 'Costa Rica',   -- [NUEVO] default local
    city            VARCHAR(100),
    address         TEXT,
    status          VARCHAR(30) NOT NULL DEFAULT 'prospect',
    -- Valores: prospect | active | inactive
    tax_id          VARCHAR(50),                          -- [NUEVO] cédula jurídica / RUC
    owner_user_id   UUID REFERENCES users(id) ON DELETE SET NULL,
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
```

> **Observación:** `tax_id` es crítico para emitir cotizaciones formales con datos fiscales del cliente.

---

### contacts

```sql
CREATE TABLE contacts (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id   UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    full_name   VARCHAR(150) NOT NULL,
    position    VARCHAR(100),
    email       VARCHAR(150),
    phone       VARCHAR(50),
    whatsapp    VARCHAR(50),
    is_primary  BOOLEAN NOT NULL DEFAULT FALSE,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,           -- [NUEVO] baja lógica
    notes       TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_primary_contact_per_client
        EXCLUDE USING gist (client_id WITH =, is_primary WITH =)
        WHERE (is_primary = TRUE)                        -- [NUEVO] enforce único contacto principal
);
```

> **Observación:** La constraint `EXCLUDE` garantiza un solo contacto primario por cliente a nivel de base de datos, no solo por lógica de aplicación. Alternativamente puede manejarse con un trigger si la constraint `EXCLUDE` es compleja de migrar.

---

### leads

```sql
CREATE TABLE leads (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name             VARCHAR(150) NOT NULL,
    company_name          VARCHAR(180),
    email                 VARCHAR(150),
    phone                 VARCHAR(50),
    whatsapp              VARCHAR(50),
    source                VARCHAR(80),
    -- Valores sugeridos: website | whatsapp | facebook_ads | instagram |
    --                    linkedin | referral | email | phone_call
    interest              TEXT,
    message               TEXT,
    status                VARCHAR(30) NOT NULL DEFAULT 'new',
    -- Valores: new | contacted | qualified | unqualified | converted
    assigned_user_id      UUID REFERENCES users(id) ON DELETE SET NULL,
    converted_client_id   UUID REFERENCES clients(id) ON DELETE SET NULL,
    converted_contact_id  UUID REFERENCES contacts(id) ON DELETE SET NULL,
    converted_at          TIMESTAMP,                     -- [NUEVO] fecha de conversión
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### opportunities

```sql
CREATE TABLE opportunities (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id           UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    contact_id          UUID REFERENCES contacts(id) ON DELETE SET NULL,
    lead_id             UUID REFERENCES leads(id) ON DELETE SET NULL,
    title               VARCHAR(180) NOT NULL,
    description         TEXT,
    stage               VARCHAR(50) NOT NULL DEFAULT 'new',
    -- Valores: new | contacted | meeting_scheduled | diagnosis_done |
    --          quote_sent | negotiation | won | lost
    estimated_value     NUMERIC(12,2) DEFAULT 0,
    probability         INTEGER DEFAULT 0 CHECK (probability BETWEEN 0 AND 100),
    expected_close_date DATE,
    closed_at           TIMESTAMP,                       -- [NUEVO] fecha real de cierre
    owner_user_id       UUID REFERENCES users(id) ON DELETE SET NULL,
    lost_reason         TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### services

```sql
CREATE TABLE services (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name         VARCHAR(180) NOT NULL,
    description  TEXT,
    category     VARCHAR(100),
    base_price   NUMERIC(12,2) NOT NULL DEFAULT 0,
    billing_type VARCHAR(30) NOT NULL DEFAULT 'one_time',
    -- Valores: one_time | monthly | annual
    currency     VARCHAR(10) NOT NULL DEFAULT 'USD',     -- [NUEVO] moneda por servicio
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order   INTEGER DEFAULT 0,                      -- [NUEVO] orden en el catálogo
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### quotes

```sql
CREATE TABLE quotes (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    quote_number        VARCHAR(50) UNIQUE NOT NULL,
    -- Formato recomendado: COT-2026-0001
    client_id           UUID NOT NULL REFERENCES clients(id),
    contact_id          UUID REFERENCES contacts(id) ON DELETE SET NULL,
    opportunity_id      UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    status              VARCHAR(30) NOT NULL DEFAULT 'draft',
    -- Valores: draft | sent | approved | rejected | expired
    currency            VARCHAR(10) NOT NULL DEFAULT 'USD',
    subtotal            NUMERIC(12,2) NOT NULL DEFAULT 0,
    tax_rate            NUMERIC(5,2) NOT NULL DEFAULT 0,
    tax_amount          NUMERIC(12,2) NOT NULL DEFAULT 0,
    discount_amount     NUMERIC(12,2) NOT NULL DEFAULT 0,
    total               NUMERIC(12,2) NOT NULL DEFAULT 0,
    valid_until         DATE,
    sent_at             TIMESTAMP,                       -- [NUEVO] fecha de envío
    approved_at         TIMESTAMP,                       -- [NUEVO] fecha de aprobación
    terms               TEXT,
    notes               TEXT,
    created_by_user_id  UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### quote_items

```sql
CREATE TABLE quote_items (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    quote_id     UUID NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    service_id   UUID REFERENCES services(id) ON DELETE SET NULL,
    description  TEXT NOT NULL,
    quantity     NUMERIC(10,2) NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price   NUMERIC(12,2) NOT NULL DEFAULT 0,
    billing_type VARCHAR(30) NOT NULL DEFAULT 'one_time',
    line_total   NUMERIC(12,2) NOT NULL DEFAULT 0,
    sort_order   INTEGER DEFAULT 0
);
```

---

### tasks

```sql
CREATE TABLE tasks (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title             VARCHAR(180) NOT NULL,
    description       TEXT,
    status            VARCHAR(30) NOT NULL DEFAULT 'pending',
    -- Valores: pending | in_progress | completed | cancelled
    priority          VARCHAR(30) NOT NULL DEFAULT 'medium',
    -- Valores: low | medium | high
    due_date          TIMESTAMP,
    completed_at      TIMESTAMP,                         -- [NUEVO] fecha real de completado
    assigned_user_id  UUID REFERENCES users(id) ON DELETE SET NULL,
    client_id         UUID REFERENCES clients(id) ON DELETE SET NULL,
    contact_id        UUID REFERENCES contacts(id) ON DELETE SET NULL,
    lead_id           UUID REFERENCES leads(id) ON DELETE SET NULL,
    opportunity_id    UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### activities

```sql
CREATE TABLE activities (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_type   VARCHAR(50) NOT NULL,
    -- Valores: call | email | whatsapp | meeting | note |
    --          status_change | quote_sent | task_completed
    subject         VARCHAR(180),
    description     TEXT,
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    client_id       UUID REFERENCES clients(id) ON DELETE SET NULL,
    contact_id      UUID REFERENCES contacts(id) ON DELETE SET NULL,
    lead_id         UUID REFERENCES leads(id) ON DELETE SET NULL,
    opportunity_id  UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    quote_id        UUID REFERENCES quotes(id) ON DELETE SET NULL,
    activity_date   TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### system_config

```sql
-- [NUEVA TABLA] Configuración global del sistema
CREATE TABLE system_config (
    key         VARCHAR(100) PRIMARY KEY,
    value       TEXT NOT NULL,
    description TEXT,
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Valores iniciales sugeridos
INSERT INTO system_config (key, value, description) VALUES
  ('default_currency',   'USD',          'Moneda por defecto en cotizaciones'),
  ('tax_rate_default',   '13',           'IVA por defecto (%)'),
  ('quote_prefix',       'COT',          'Prefijo para número de cotización'),
  ('company_name',       'Bemantis',     'Nombre de la empresa'),
  ('quote_valid_days',   '30',           'Días de validez por defecto de cotización');
```

> **Observación:** Centralizar configuración en `system_config` permite cambiar moneda, impuesto o prefijos sin deployar código.

---

### Índices

```sql
CREATE INDEX idx_clients_owner          ON clients(owner_user_id);
CREATE INDEX idx_clients_status         ON clients(status);
CREATE INDEX idx_contacts_client        ON contacts(client_id);
CREATE INDEX idx_leads_status           ON leads(status);
CREATE INDEX idx_leads_assigned         ON leads(assigned_user_id);
CREATE INDEX idx_opportunities_stage    ON opportunities(stage);
CREATE INDEX idx_opportunities_client   ON opportunities(client_id);
CREATE INDEX idx_quotes_status          ON quotes(status);
CREATE INDEX idx_quotes_client          ON quotes(client_id);
CREATE INDEX idx_tasks_assigned_user    ON tasks(assigned_user_id);
CREATE INDEX idx_tasks_status           ON tasks(status);
CREATE INDEX idx_tasks_due_date         ON tasks(due_date);
CREATE INDEX idx_activities_client      ON activities(client_id);
CREATE INDEX idx_activities_opportunity ON activities(opportunity_id);
CREATE INDEX idx_activities_type        ON activities(activity_type);
```

---

## Endpoints FastAPI

Base URL: `/api/v1`

### Auth

```
POST   /auth/login          → {access_token, token_type, expires_in, user}
POST   /auth/refresh        → {access_token}
GET    /auth/me             → UserResponse
POST   /auth/logout         → 204
POST   /auth/change-password  → 200  [NUEVO]
```

---

### Usuarios — solo admin

```
GET    /users                          ?search=&role=&is_active=
POST   /users
GET    /users/{user_id}
PUT    /users/{user_id}
PATCH  /users/{user_id}/activate
PATCH  /users/{user_id}/deactivate
DELETE /users/{user_id}               (soft delete recomendado)
```

---

### Clientes

```
GET    /clients                        ?search=&status=&industry=&owner_user_id=&page=&size=
POST   /clients
GET    /clients/{client_id}
PUT    /clients/{client_id}
DELETE /clients/{client_id}
GET    /clients/{client_id}/contacts
GET    /clients/{client_id}/opportunities
GET    /clients/{client_id}/quotes
GET    /clients/{client_id}/tasks      [NUEVO]
GET    /clients/{client_id}/activities
```

---

### Contactos

```
GET    /contacts                       ?client_id=&search=&is_active=
POST   /contacts
GET    /contacts/{contact_id}
PUT    /contacts/{contact_id}
DELETE /contacts/{contact_id}
PATCH  /contacts/{contact_id}/set-primary  [NUEVO] promueve como principal
```

---

### Leads

```
GET    /leads                          ?status=&source=&assigned_user_id=&search=&page=&size=
POST   /leads
GET    /leads/{lead_id}
PUT    /leads/{lead_id}
DELETE /leads/{lead_id}
PATCH  /leads/{lead_id}/status
POST   /leads/{lead_id}/convert
```

**Body de conversión:**
```json
{
  "create_client": true,
  "create_contact": true,
  "create_opportunity": true,
  "opportunity_title": "Sitio web + agente IA",
  "opportunity_stage": "new"
}
```

---

### Oportunidades

```
GET    /opportunities                  ?stage=&client_id=&owner_user_id=&expected_close_from=&expected_close_to=&page=&size=
POST   /opportunities
GET    /opportunities/{opportunity_id}
PUT    /opportunities/{opportunity_id}
DELETE /opportunities/{opportunity_id}
PATCH  /opportunities/{opportunity_id}/stage
PATCH  /opportunities/{opportunity_id}/won
PATCH  /opportunities/{opportunity_id}/lost
GET    /opportunities/pipeline         → agrupa por etapa con totales
```

---

### Servicios

```
GET    /services                       ?category=&billing_type=&is_active=&search=
POST   /services
GET    /services/{service_id}
PUT    /services/{service_id}
PATCH  /services/{service_id}/activate
PATCH  /services/{service_id}/deactivate
DELETE /services/{service_id}
```

---

### Cotizaciones

```
GET    /quotes                         ?status=&client_id=&opportunity_id=&created_by_user_id=&date_from=&date_to=&page=&size=
POST   /quotes
GET    /quotes/{quote_id}
PUT    /quotes/{quote_id}
DELETE /quotes/{quote_id}
POST   /quotes/{quote_id}/items
PUT    /quotes/{quote_id}/items/{item_id}
DELETE /quotes/{quote_id}/items/{item_id}
PATCH  /quotes/{quote_id}/send
PATCH  /quotes/{quote_id}/approve
PATCH  /quotes/{quote_id}/reject
POST   /quotes/{quote_id}/duplicate
GET    /quotes/{quote_id}/pdf          (Fase 2 — WeasyPrint / ReportLab)
PATCH  /quotes/{quote_id}/expire       [NUEVO] marcar como vencida manualmente
```

---

### Tareas

```
GET    /tasks                          ?status=&priority=&assigned_user_id=&due_from=&due_to=&client_id=&opportunity_id=
POST   /tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
PATCH  /tasks/{task_id}/complete
PATCH  /tasks/{task_id}/cancel
```

---

### Actividades

```
GET    /activities                     ?client_id=&lead_id=&opportunity_id=&quote_id=&activity_type=&user_id=&date_from=&date_to=
POST   /activities
GET    /activities/{activity_id}
PUT    /activities/{activity_id}
DELETE /activities/{activity_id}
```

---

### Reportes

```
GET    /reports/dashboard
GET    /reports/leads-by-source
GET    /reports/opportunities-by-stage
GET    /reports/quotes-by-status
GET    /reports/sales-forecast         ?year=&month=
GET    /reports/tasks-summary
GET    /reports/top-clients            [NUEVO] clientes con más valor cotizado
```

**Respuesta del dashboard:**
```json
{
  "total_leads":               45,
  "open_opportunities":        18,
  "quoted_amount":          24500,
  "won_amount":              8600,
  "pending_tasks":             12,
  "quotes_waiting_approval":    6,
  "conversion_rate":         0.38,
  "avg_deal_size":           1361
}
```

---

### Configuración del sistema

```
GET    /config                         [NUEVO] lista todos los parámetros (solo admin)
PATCH  /config/{key}                   [NUEVO] actualiza un parámetro (solo admin)
```

---

## Lógica de negocio — servicios internos

### quote_calculator.py

```python
def calculate_quote(items, discount_amount, tax_rate):
    subtotal = sum(item.quantity * item.unit_price for item in items)
    taxable  = subtotal - discount_amount
    tax_amt  = taxable * (tax_rate / 100)
    total    = taxable + tax_amt
    return subtotal, tax_amt, total
```

Regla: el cálculo **siempre ocurre en backend**. El frontend envía los ítems y parámetros, el backend responde con subtotal, tax_amount y total calculados y los persiste.

---

### activity_logger.py

Actividades registradas automáticamente:

| Acción | Tipo generado |
|---|---|
| Envío de cotización | `quote_sent` |
| Cambio de etapa de oportunidad | `status_change` |
| Conversión de lead | `status_change` |
| Cotización aprobada | `status_change` |
| Tarea completada | `task_completed` |

---

### lead_converter.py

Pasos al ejecutar `POST /leads/{id}/convert`:

1. Validar que el lead no esté ya en estado `converted`.
2. Si `create_client=true`: crear registro en `clients` con datos del lead.
3. Si `create_contact=true`: crear registro en `contacts` vinculado al cliente.
4. Si `create_opportunity=true`: crear oportunidad con etapa `new`.
5. Actualizar `leads.status = 'converted'` y `leads.converted_at = NOW()`.
6. Registrar actividad `status_change`.
7. Retornar IDs creados en la respuesta.

---

## Seguridad

### Autenticación

- JWT firmado con HS256 (cambiar a RS256 en Fase 4 SaaS).
- `access_token`: TTL de 8 horas.
- `refresh_token`: TTL de 30 días, rotado en cada uso.
- Contraseñas hasheadas con **bcrypt** (work factor 12).
- Middleware valida `is_active=true` en cada request.

### Permisos por rol

| Recurso | admin | manager | sales | viewer |
|---|:---:|:---:|:---:|:---:|
| Usuarios | ✅ | ❌ | ❌ | ❌ |
| Clientes | ✅ | ✅ | ✅ | 👁 |
| Leads | ✅ | ✅ | ✅ | 👁 |
| Oportunidades | ✅ | ✅ | ✅ | 👁 |
| Servicios | ✅ | ✅ | ❌ | 👁 |
| Cotizaciones | ✅ | ✅ | ✅ | 👁 |
| Reportes completos | ✅ | ✅ | ❌ | 👁 |
| Configuración | ✅ | ❌ | ❌ | ❌ |

### Scoping de datos

- Usuarios con rol `sales` solo deben ver clientes/oportunidades asignados a ellos (`owner_user_id = current_user.id`), salvo que el admin o manager los comparta.
- Implementar este filtro como dependencia reutilizable en `permissions.py`.

---

## Observaciones y recomendaciones

### ✅ Fortalezas del esquema original

- Entidades bien definidas y cobertura funcional completa para un MVP.
- Separación clara entre Services (catálogo) y Quote Items (detalle editable).
- Flujo lead → oportunidad → cotización bien trazado.
- Pipeline con 8 etapas adecuado para servicios profesionales.

### ⚠️ Puntos a reforzar

1. **Constraint de contacto principal** debe garantizarse a nivel DB, no solo aplicación.
2. **`tax_id` en clients** es necesario desde el MVP para cotizaciones con datos fiscales.
3. **Fechas de auditoría** (`sent_at`, `approved_at`, `closed_at`, `converted_at`) son críticas para reportes de ciclo de venta.
4. **Scoping por usuario `sales`** debe implementarse desde el inicio para evitar fugas de datos entre vendedores.
5. **`system_config`** evita hardcodear moneda e impuesto en código.
6. **Numeración de cotizaciones** (`COT-2026-0001`): generar con función PostgreSQL o secuencia para evitar colisiones en alta concurrencia.
7. **Soft delete vs hard delete**: recomendar soft delete (campo `deleted_at`) en clients, contacts y leads para preservar trazabilidad histórica de cotizaciones y actividades.

### 🔜 Fase 2 — pendientes técnicos

- Generación de PDF con **WeasyPrint** (plantilla HTML → PDF).
- Envío de cotizaciones por email (SMTP / SendGrid).
- Expiración automática de cotizaciones con tarea programada (APScheduler o Heroku Scheduler).
- Integración con formularios web mediante webhook autenticado.

### 🚀 Fase 3 — IA y WhatsApp

- Webhook receptor de mensajes WhatsApp Cloud API.
- Creación automática de leads desde WhatsApp.
- Agente IA (n8n) para calificación y respuestas automáticas.
- Registro automático de conversaciones como actividades tipo `whatsapp`.

---

## Dependencias Python sugeridas

```txt
fastapi
uvicorn[standard]
gunicorn
sqlalchemy[asyncio]
asyncpg
alembic
pydantic[email]
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart
httpx
```
