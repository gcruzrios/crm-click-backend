"""
Seed script: 40 cotizaciones con ítems de servicios reales.
Statuses: draft(8) | sent(12) | approved(10) | rejected(5) | expired(5)
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_quotes.py
"""
import asyncio
import uuid
from datetime import date, datetime
from decimal import Decimal
import asyncpg

DB_URL   = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"
ADMIN_ID = "d06edc36-d03f-4960-864b-e71e8baee07b"
TAX_RATE = Decimal("13.00")   # IVA Costa Rica 13%

TERMS_CR = (
    "Condiciones de pago: 50% anticipo al inicio del proyecto, 50% contra entrega. "
    "Vigencia de la cotización: 30 días calendario. "
    "Precios expresados en Dólares Americanos (USD) e incluyen IVA del 13%. "
    "Cualquier alcance adicional será cotizado por separado."
)
TERMS_MENSUAL = (
    "Servicios recurrentes: facturación mensual los primeros 5 días de cada mes. "
    "Contrato mínimo de 3 meses. Precios en USD, IVA incluido. "
    "Cancelación con 30 días de preaviso por escrito."
)

# ─── Definición de 40 cotizaciones ───────────────────────────────────────────
# Cada cotización: client(partial), status, discount_pct, tax_rate, valid_until,
#                  sent_at, approved_at, notes, terms, items[]
# Cada ítem: (service_name_partial, qty, override_price_or_None)
# ─────────────────────────────────────────────────────────────────────────────
QUOTES = [
    # ════════════════════════════ DRAFT (8) ════════════════════════════════════
    {
        "client": "Bufete Jurídico Sánchez",
        "status": "draft", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 15), "sent_at": None, "approved_at": None,
        "notes": "Propuesta inicial preparada para reunión de presentación pendiente.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("Hosting y Dominio Premium", 1, None),
            ("SEO Local", 3, None),          # 3 meses
            ("Optimización Google Business", 1, None),
        ],
    },
    {
        "client": "Inversiones Centroamérica Holdings",
        "status": "draft", "discount_pct": 10, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 30), "sent_at": None, "approved_at": None,
        "notes": "Cotización corporativa con descuento especial por volumen. Sujeta a revisión del equipo legal del cliente.",
        "terms": TERMS_CR,
        "items": [
            ("Plan de Marketing Digital 360°", 1, None),
            ("Diseño Web Corporativo", 1, None),
            ("SEO Nacional", 6, None),        # 6 meses
            ("Gestión de Google Ads", 3, None),
        ],
    },
    {
        "client": "Importadora Pacífico Norte",
        "status": "draft", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 20), "sent_at": None, "approved_at": None,
        "notes": "Propuesta en revisión interna antes de enviar al cliente.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("Landing Page de Alta Conversión", 2, None),
            ("SEO Nacional", 4, None),
            ("Hosting y Dominio Premium", 1, None),
        ],
    },
    {
        "client": "Grupo Pérez Hermanos",
        "status": "draft", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 1), "sent_at": None, "approved_at": None,
        "notes": "Cotización digital para equipo de vendedores. Incluye descuento de bienvenida del 5%.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Redes Sociales (Plan Profesional)", 3, None),
            ("Gestión de Meta Ads", 3, None),
            ("Estrategia de Contenido Digital", 1, None),
            ("Sesión Fotográfica", 1, None),
        ],
    },
    {
        "client": "Supermercados La Colonia",
        "status": "draft", "discount_pct": 8, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 10), "sent_at": None, "approved_at": None,
        "notes": "Propuesta para cadena de supermercados. Descuento por contrato anual de e-commerce.",
        "terms": TERMS_CR,
        "items": [
            ("Tienda en Línea (E-commerce)", 1, None),
            ("SEO para E-commerce", 6, None),
            ("Mantenimiento Web Mensual", 6, None),
            ("Gestión de Google Ads", 3, None),
        ],
    },
    {
        "client": "Servicios Integrales Mora",
        "status": "draft", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 25), "sent_at": None, "approved_at": None,
        "notes": "Cotización básica de inicio para consultora pequeña.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Local", 3, None),
            ("Optimización Google Business", 1, None),
            ("Gestión de Redes Sociales (Plan Básico)", 3, None),
        ],
    },
    {
        "client": "Distribuciones VH",
        "status": "draft", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 5), "sent_at": None, "approved_at": None,
        "notes": "Cotización para empresa distribuidora con enfoque en redes sociales y captación de clientas.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Redes Sociales (Plan Básico)", 3, None),
            ("Sesión Fotográfica", 1, None),
            ("Gestión de Meta Ads", 3, None),
        ],
    },
    {
        "client": "Media Digital Torres",
        "status": "draft", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 15), "sent_at": None, "approved_at": None,
        "notes": "Propuesta de IA para agencia de marketing. Pendiente de validación técnica.",
        "terms": TERMS_CR,
        "items": [
            ("Chatbot con IA para WhatsApp y Web", 1, None),
            ("Mantenimiento de Chatbot IA", 3, None),
            ("Automatización de Marketing con IA", 1, None),
        ],
    },

    # ════════════════════════════ SENT (12) ════════════════════════════════════
    {
        "client": "Agencia Inmobiliaria Campos",
        "status": "sent", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 31), "sent_at": datetime(2026, 7, 1, 9, 0), "approved_at": None,
        "notes": "Cotización enviada por correo. Esperando respuesta del Lic. Jorge Campos.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 6, None),
            ("Hosting y Dominio Premium", 1, None),
            ("Mantenimiento Web Mensual", 6, None),
        ],
    },
    {
        "client": "Tech Solutions Guzmán",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 28), "sent_at": datetime(2026, 6, 28, 10, 30), "approved_at": None,
        "notes": "Solución de automatización con IA presentada en demo el 25 jun. Cliente revisando propuesta con su equipo técnico.",
        "terms": TERMS_CR,
        "items": [
            ("Automatización de Marketing con IA", 1, None),
            ("Chatbot con IA para WhatsApp y Web", 1, None),
            ("Mantenimiento de Chatbot IA", 6, None),
            ("Optimización para IA Search (GEO / AI SEO)", 3, None),
        ],
    },
    {
        "client": "Agrícola Los Naranjos",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 5), "sent_at": datetime(2026, 7, 5, 8, 0), "approved_at": None,
        "notes": "Propuesta de posicionamiento internacional para exportadora de piña. Énfasis en mercado europeo y asiático.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Internacional", 6, None),
            ("Plan de Marketing Digital 360°", 1, None),
            ("Gestión de Redes Sociales (Plan Profesional)", 3, None),
            ("Gestión de Google Ads", 3, None),
        ],
    },
    {
        "client": "Arias & Méndez Arquitectos",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 25), "sent_at": datetime(2026, 6, 25, 14, 0), "approved_at": None,
        "notes": "Presentación enviada por correo certificado y WhatsApp. Seguimiento agendado para el 15 de julio.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 4, None),
            ("Gestión de Redes Sociales (Plan Básico)", 3, None),
            ("Sesión Fotográfica", 2, None),
        ],
    },
    {
        "client": "Equipos Médicos Bermúdez",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 20), "sent_at": datetime(2026, 6, 20, 11, 0), "approved_at": None,
        "notes": "Propuesta de generación de leads para equipo de visitadores médicos. Pendiente aprobación de gerencia.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Google Ads", 3, None),
            ("Gestión de Meta Ads", 3, None),
            ("Landing Page de Alta Conversión", 3, None),
            ("Configuración Inicial de Campañas", 1, None),
        ],
    },
    {
        "client": "Brenes Logística Internacional",
        "status": "sent", "discount_pct": 10, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 10), "sent_at": datetime(2026, 7, 10, 9, 30), "approved_at": None,
        "notes": "Propuesta con descuento del 10% por contrato semestral. En proceso de validación legal por contratos en Panamá y Colombia.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Nacional", 6, None),
            ("Gestión de Google Ads", 6, None),
            ("Consultoría Mensual de Marketing Digital", 6, None),
            ("Plan de Marketing Digital 360°", 1, None),
        ],
    },
    {
        "client": "Ferretería Industrial Ramírez",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 30), "sent_at": datetime(2026, 6, 30, 16, 0), "approved_at": None,
        "notes": "Propuesta de presencia digital para ferretería industrial. Cliente comparando con otra agencia.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 4, None),
            ("Hosting y Dominio Premium", 1, None),
            ("Optimización Google Business", 1, None),
        ],
    },
    {
        "client": "Clínica Dental Mora",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 1), "sent_at": datetime(2026, 7, 1, 10, 0), "approved_at": None,
        "notes": "Cotización para posicionamiento de clínica dental en redes sociales. Énfasis en ortodoncia y estética dental.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Redes Sociales (Plan Profesional)", 6, None),
            ("Gestión de Meta Ads", 3, None),
            ("Sesión Fotográfica", 2, None),
            ("SEO Local", 3, None),
        ],
    },
    {
        "client": "Centro Educativo Bilingüe Prado",
        "status": "sent", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 20), "sent_at": datetime(2026, 7, 20, 8, 0), "approved_at": None,
        "notes": "Propuesta para inicio de ciclo lectivo 2027. Incluye descuento institucional del 5%.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 6, None),
            ("Gestión de Redes Sociales (Plan Básico)", 6, None),
            ("Estrategia de Contenido Digital", 1, None),
        ],
    },
    {
        "client": "Consultoría RH Blanco",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 15), "sent_at": datetime(2026, 7, 15, 11, 30), "approved_at": None,
        "notes": "Propuesta de generación de prospectos B2B para firma de RRHH. Cliente evaluando ROI esperado.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Landing Page de Alta Conversión", 2, None),
            ("Gestión de Google Ads", 4, None),
            ("Gestión de Meta Ads", 4, None),
            ("Configuración Inicial de Campañas", 1, None),
        ],
    },
    {
        "client": "Comercializadora Rodríguez",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 25), "sent_at": datetime(2026, 7, 25, 9, 0), "approved_at": None,
        "notes": "Cotización para distribuidora con fuerza de ventas de 8 personas. Énfasis en captación vía redes sociales.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Redes Sociales (Plan Profesional)", 6, None),
            ("Gestión de Meta Ads", 6, None),
            ("Estrategia de Contenido Digital", 1, None),
        ],
    },
    {
        "client": "Servicios de Limpieza Ruiz",
        "status": "sent", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 8, 30), "sent_at": datetime(2026, 7, 30, 14, 0), "approved_at": None,
        "notes": "Propuesta de captación de contratos corporativos de limpieza vía publicidad digital.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Local", 4, None),
            ("Optimización Google Business", 1, None),
            ("Gestión de Meta Ads", 4, None),
            ("Landing Page de Alta Conversión", 1, None),
        ],
    },

    # ════════════════════════════ APPROVED (10) ═════════════════════════════════
    {
        "client": "Importaciones JB del Caribe",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 30), "sent_at": datetime(2026, 5, 20, 9, 0), "approved_at": datetime(2026, 5, 28, 11, 0),
        "notes": "Cotización aprobada por el Lic. Roberto Jiménez vía correo. Proyecto iniciado el 1 de junio.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Nacional", 6, None),
            ("Gestión de Google Ads", 6, None),
            ("Hosting y Dominio Premium", 1, None),
        ],
    },
    {
        "client": "Grupo Pérez Hermanos",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 15), "sent_at": datetime(2026, 5, 5, 10, 0), "approved_at": datetime(2026, 5, 12, 14, 30),
        "notes": "Aprobada por Alejandro Pérez. Contrato firmado. Servicio activo desde mayo 2026.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Nacional", 6, None),
            ("Gestión de Google Ads", 6, None),
            ("Gestión de Redes Sociales (Plan Profesional)", 6, None),
            ("Consultoría Mensual de Marketing Digital", 6, None),
        ],
    },
    {
        "client": "Logística Express Centroamérica",
        "status": "approved", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 4, 30), "sent_at": datetime(2026, 3, 5, 9, 0), "approved_at": datetime(2026, 3, 12, 10, 0),
        "notes": "Aprobada. Contrato con cobertura para CR, PAN, HN, SV. Descuento especial multipaís.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Nacional", 6, None),
            ("Gestión de Meta Ads", 6, None),
        ],
    },
    {
        "client": "Constructora Los Pinos",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 20), "sent_at": datetime(2026, 4, 10, 9, 0), "approved_at": datetime(2026, 4, 18, 16, 0),
        "notes": "Aprobada por el Ing. Mauricio Jiménez. Sitio web en producción.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("Gestión de Google Ads", 3, None),
            ("Gestión de Redes Sociales (Plan Básico)", 3, None),
            ("Optimización Google Business", 1, None),
        ],
    },
    {
        "client": "Exportaciones Café Verde",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 15), "sent_at": datetime(2026, 5, 10, 8, 30), "approved_at": datetime(2026, 5, 15, 9, 0),
        "notes": "Proyecto de posicionamiento internacional aprobado. María Fernanda Quesada firmó contrato.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Internacional", 6, None),
            ("Plan de Marketing Digital 360°", 1, None),
            ("Gestión de Google Ads", 6, None),
        ],
    },
    {
        "client": "Grupo Empresarial Alianza",
        "status": "approved", "discount_pct": 15, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 30), "sent_at": datetime(2026, 4, 20, 10, 0), "approved_at": datetime(2026, 4, 28, 15, 0),
        "notes": "Cliente estratégico. Descuento del 15% por contrato anual de IA. Proyecto en fase de implementación.",
        "terms": TERMS_CR,
        "items": [
            ("Chatbot con IA para WhatsApp y Web", 1, None),
            ("Automatización de Marketing con IA", 1, None),
            ("Mantenimiento de Chatbot IA", 12, None),
            ("Consultoría de Transformación Digital con IA", 1, None),
        ],
    },
    {
        "client": "Clínica de Salud Integral Bienestar",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 10), "sent_at": datetime(2026, 6, 10, 9, 0), "approved_at": datetime(2026, 6, 18, 14, 0),
        "notes": "Aprobada por Laura Chinchilla. Proyecto integral de presencia digital para clínica.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 6, None),
            ("Gestión de Meta Ads", 6, None),
            ("Gestión de Redes Sociales (Plan Profesional)", 6, None),
        ],
    },
    {
        "client": "Instituto Educativo Latinoamérica",
        "status": "approved", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 30), "sent_at": datetime(2026, 5, 25, 8, 0), "approved_at": datetime(2026, 6, 2, 10, 0),
        "notes": "Aprobada con descuento institucional. Proyecto alineado al inicio del ciclo académico 2026-2.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 6, None),
            ("Gestión de Redes Sociales (Plan Básico)", 6, None),
            ("Hosting y Dominio Premium", 1, None),
        ],
    },
    {
        "client": "Cooperativa Agrícola del Valle",
        "status": "approved", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 5), "sent_at": datetime(2026, 6, 5, 9, 30), "approved_at": datetime(2026, 6, 15, 11, 0),
        "notes": "Aprobada por Junta Directiva de la Cooperativa en sesión del 15 jun. Contrato firmado.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Local", 6, None),
            ("Optimización Google Business", 1, None),
            ("Gestión de Redes Sociales (Plan Básico)", 6, None),
            ("Sesión Fotográfica", 1, None),
        ],
    },
    {
        "client": "Agencia Creativa Fusión Digital",
        "status": "approved", "discount_pct": 10, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 7, 1), "sent_at": datetime(2026, 6, 1, 10, 0), "approved_at": datetime(2026, 6, 8, 16, 0),
        "notes": "Agencia cliente activa. Descuento del 10% por ser cliente de referencia. Proyecto de IA iniciado.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Producción de Contenido con IA", 6, None),
            ("Optimización para IA Search (GEO / AI SEO)", 6, None),
            ("Chatbot con IA para WhatsApp y Web", 1, None),
            ("Mantenimiento de Chatbot IA", 6, None),
        ],
    },

    # ════════════════════════════ REJECTED (5) ══════════════════════════════════
    {
        "client": "Gamboa Ingeniería Civil",
        "status": "rejected", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 1), "sent_at": datetime(2026, 5, 1, 9, 0), "approved_at": None,
        "notes": "Rechazada. El cliente contrató con firma extranjera a menor costo. Posible retoma en 2027.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Nacional", 4, None),
            ("Gestión de Google Ads", 4, None),
        ],
    },
    {
        "client": "Medios y Comunicaciones Caribe",
        "status": "rejected", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 15), "sent_at": datetime(2026, 4, 15, 10, 0), "approved_at": None,
        "notes": "Rechazada por congelamiento de presupuesto. Grupo de medios en reestructuración financiera.",
        "terms": TERMS_CR,
        "items": [
            ("Chatbot con IA para WhatsApp y Web", 1, None),
            ("Automatización de Marketing con IA", 1, None),
            ("Optimización para IA Search (GEO / AI SEO)", 3, None),
        ],
    },
    {
        "client": "Distribuidora El Mercado Tropical",
        "status": "rejected", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 4, 1), "sent_at": datetime(2026, 3, 1, 9, 0), "approved_at": None,
        "notes": "Rechazada. Empresa en proceso de fusión. Todos los proyectos de inversión congelados.",
        "terms": TERMS_CR,
        "items": [
            ("Tienda en Línea (E-commerce)", 1, None),
            ("SEO para E-commerce", 6, None),
            ("Gestión de Google Ads", 3, None),
        ],
    },
    {
        "client": "Asesoría Contable Salas",
        "status": "rejected", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 10), "sent_at": datetime(2026, 5, 10, 9, 0), "approved_at": None,
        "notes": "Propuesta rechazada por presupuesto limitado. La clienta optó por perfil gratuito en redes.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 3, None),
            ("Hosting y Dominio Premium", 1, None),
        ],
    },
    {
        "client": "Finanzas y Crédito Mora",
        "status": "rejected", "discount_pct": 5, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 6, 20), "sent_at": datetime(2026, 5, 20, 11, 0), "approved_at": None,
        "notes": "Rechazada. El cliente eligió un proveedor con menor precio sin IVA. Seguimiento en Q4 2026.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("Gestión de Google Ads", 6, None),
            ("Gestión de Meta Ads", 6, None),
        ],
    },

    # ════════════════════════════ EXPIRED (5) ═══════════════════════════════════
    {
        "client": "Soluciones Financieras del Sur",
        "status": "expired", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 4, 30), "sent_at": datetime(2026, 3, 30, 9, 0), "approved_at": None,
        "notes": "Cotización vencida sin respuesta. El contacto en Colombia dejó la empresa. Reenviar actualizada.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Plan de Marketing Digital 360°", 1, None),
            ("Gestión de Google Ads", 6, None),
            ("SEO Nacional", 6, None),
        ],
    },
    {
        "client": "Hotel & Spa Las Brisas",
        "status": "expired", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 31), "sent_at": datetime(2026, 4, 30, 10, 0), "approved_at": None,
        "notes": "Propuesta de alta temporada vencida. Reactivar contacto con el Sr. Mena en agosto para temporada dic-abr.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("Gestión de Redes Sociales (Plan Profesional)", 6, None),
            ("Gestión de Meta Ads", 6, None),
            ("Sesión Fotográfica", 3, None),
            ("Estrategia de Contenido Digital", 1, None),
        ],
    },
    {
        "client": "Seguridad Privada Fortis",
        "status": "expired", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 15), "sent_at": datetime(2026, 4, 15, 8, 30), "approved_at": None,
        "notes": "Propuesta vencida. Cliente ocupado con renovación de contratos de seguridad de fin de año. Reagendar en julio.",
        "terms": TERMS_CR,
        "items": [
            ("Diseño Web Corporativo", 1, None),
            ("SEO Local", 3, None),
            ("Gestión de Meta Ads", 3, None),
        ],
    },
    {
        "client": "Desarrolladora Residencial Palmares",
        "status": "expired", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 20), "sent_at": datetime(2026, 4, 20, 14, 0), "approved_at": None,
        "notes": "Propuesta vencida. La gerente de ventas solicitó nueva versión con más énfasis en Google Ads.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Local", 4, None),
            ("Gestión de Google Ads", 4, None),
            ("Landing Page de Alta Conversión", 2, None),
        ],
    },
    {
        "client": "Farmacéutica Nacional Salud Total",
        "status": "expired", "discount_pct": 0, "tax_rate": TAX_RATE,
        "valid_until": date(2026, 5, 25), "sent_at": datetime(2026, 4, 25, 9, 0), "approved_at": None,
        "notes": "Propuesta de visitadores médicos vencida. En espera del resultado de licitación pública de julio 2026.",
        "terms": TERMS_MENSUAL,
        "items": [
            ("SEO Nacional", 6, None),
            ("Gestión de Google Ads", 6, None),
            ("Gestión de Redes Sociales (Plan Profesional)", 3, None),
        ],
    },
]


def calc_totals(items_data, discount_pct, tax_rate):
    subtotal = sum(Decimal(str(i["unit_price"])) * Decimal(str(i["qty"])) for i in items_data)
    discount = (subtotal * Decimal(str(discount_pct)) / 100).quantize(Decimal("0.01"))
    taxable  = subtotal - discount
    tax_amt  = (taxable * tax_rate / 100).quantize(Decimal("0.01"))
    total    = taxable + tax_amt
    return subtotal, discount, tax_amt, total


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # ── Cargar servicios ──────────────────────────────────────────────────
        svc_rows = await conn.fetch(
            "SELECT id, name, base_price, billing_type FROM services WHERE is_active = TRUE"
        )
        def find_service(partial):
            for r in svc_rows:
                if partial.lower() in r["name"].lower():
                    return r
            raise ValueError(f"Servicio no encontrado: {partial!r}")

        # ── Cargar clientes con contacto y oportunidad ────────────────────────
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) as contact_id,
                   (SELECT o.id  FROM opportunities o  WHERE o.client_id = c.id LIMIT 1) as opp_id
            FROM clients c
        """)
        def find_client(partial):
            for r in client_rows:
                if partial.lower() in r["name"].lower():
                    return r
            raise ValueError(f"Cliente no encontrado: {partial!r}")

        # ── Contador de cotizaciones para numeración ──────────────────────────
        existing = await conn.fetchval("SELECT COUNT(*) FROM quotes")
        seq = existing + 1

        inserted = 0
        status_count = {}

        print(f"\n  {'#':>3}  {'NÚMERO':14s}  {'STATUS':10s}  {'SUBTOTAL':>10}  {'DESC':>5}  {'IVA':>8}  {'TOTAL':>10}  CLIENTE")
        print(f"  {'─'*100}")

        async with conn.transaction():
            for q in QUOTES:
                client = find_client(q["client"])

                # Resolver ítems con datos reales de servicios
                items_data = []
                for (svc_partial, qty, override_price) in q["items"]:
                    svc = find_service(svc_partial)
                    price = Decimal(str(override_price)) if override_price else Decimal(str(svc["base_price"]))
                    items_data.append({
                        "service_id":   svc["id"],
                        "description":  svc["name"],
                        "qty":          qty,
                        "unit_price":   price,
                        "billing_type": svc["billing_type"],
                    })

                subtotal, discount, tax_amt, total = calc_totals(
                    items_data, q["discount_pct"], q["tax_rate"]
                )

                quote_num = f"COT-2026-{seq:03d}"
                quote_id  = uuid.uuid4()

                await conn.execute("""
                    INSERT INTO quotes (
                        id, quote_number, client_id, contact_id, opportunity_id,
                        status, currency, subtotal, tax_rate, tax_amount,
                        discount_amount, total, valid_until, sent_at, approved_at,
                        terms, notes, created_by_user_id
                    ) VALUES (
                        $1,$2,$3,$4,$5,$6,'USD',$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17
                    )
                """,
                    quote_id, quote_num,
                    client["id"], client["contact_id"], client["opp_id"],
                    q["status"],
                    float(subtotal), float(q["tax_rate"]),
                    float(tax_amt), float(discount), float(total),
                    q["valid_until"], q["sent_at"], q["approved_at"],
                    q["terms"], q["notes"],
                    uuid.UUID(ADMIN_ID),
                )

                for idx, item in enumerate(items_data):
                    line = item["unit_price"] * Decimal(str(item["qty"]))
                    await conn.execute("""
                        INSERT INTO quote_items (
                            id, quote_id, service_id, description,
                            quantity, unit_price, billing_type, line_total, sort_order
                        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                    """,
                        uuid.uuid4(), quote_id, item["service_id"],
                        item["description"], float(item["qty"]),
                        float(item["unit_price"]), item["billing_type"],
                        float(line), (idx + 1) * 10,
                    )

                status_count[q["status"]] = status_count.get(q["status"], 0) + 1
                inserted += 1
                seq += 1

                disc_str = f"-{q['discount_pct']}%" if q["discount_pct"] else "  —  "
                print(f"  {inserted:>3}  {quote_num:14s}  {q['status']:10s}  "
                      f"${float(subtotal):>8,.2f}  {disc_str:>5}  "
                      f"${float(tax_amt):>6,.2f}  ${float(total):>8,.2f}  "
                      f"{client['name'][:40]}")

        # ── Resumen ───────────────────────────────────────────────────────────
        print(f"\n{'═'*60}")
        totals = await conn.fetch("""
            SELECT status, COUNT(*) as n,
                   SUM(total) as total_sum, SUM(subtotal) as sub_sum
            FROM quotes GROUP BY status ORDER BY total_sum DESC
        """)
        grand_total = await conn.fetchval("SELECT SUM(total) FROM quotes")
        print(f"  {'STATUS':12s} {'#':>4}  {'SUBTOTAL':>13}  {'TOTAL':>13}")
        print(f"  {'─'*55}")
        for r in totals:
            print(f"  {r['status']:12s} {r['n']:>4}  ${float(r['sub_sum']):>11,.2f}  ${float(r['total_sum']):>11,.2f}")
        print(f"  {'─'*55}")
        print(f"  {'TOTAL':12s} {inserted:>4}  {'':>13}  ${float(grand_total):>11,.2f}")
        print(f"{'═'*60}")
        print(f"\n✓ {inserted} cotizaciones insertadas con sus ítems de servicio.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
