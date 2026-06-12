"""
Seed script: 30 servicios basados en el catálogo de ClickDigital (www.clickdigitalcr.com).
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_services.py
"""
import asyncio
import uuid
import asyncpg

DB_URL = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"

SERVICES = [
    # ─── CATEGORÍA: Diseño y Desarrollo Web ───────────────────────────────────
    {
        "name": "Diseño Web Corporativo",
        "description": "Sitio web profesional en WordPress, hasta 8 páginas, diseño responsivo, optimizado para Google y velocidad. Incluye formulario de contacto, integración con redes sociales y capacitación básica de uso.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 1200.00,
        "billing_type": "one_time",
        "sort_order": 10,
    },
    {
        "name": "Tienda en Línea (E-commerce)",
        "description": "Tienda WooCommerce con hasta 50 productos, integración con pasarelas de pago (Stripe, PayPal, BAC, TiloPay), carrito de compras, gestión de inventario y diseño responsive.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 2500.00,
        "billing_type": "one_time",
        "sort_order": 20,
    },
    {
        "name": "Landing Page de Alta Conversión",
        "description": "Página de aterrizaje optimizada para conversiones, diseñada para campañas de Google Ads o Meta Ads. Incluye formulario de captura, prueba A/B básica e integración con CRM.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 650.00,
        "billing_type": "one_time",
        "sort_order": 30,
    },
    {
        "name": "Mantenimiento Web Mensual",
        "description": "Actualización de plugins y temas WordPress, copias de seguridad semanales, monitoreo de seguridad, correcciones menores de contenido (hasta 2 horas/mes) e informe mensual de estado.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 120.00,
        "billing_type": "monthly",
        "sort_order": 40,
    },
    {
        "name": "Hosting y Dominio Premium",
        "description": "Alojamiento web con servidor de alta velocidad, SSL gratuito, correos corporativos, soporte técnico local en Costa Rica, panel cPanel y dominio .com o .cr por 1 año.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 180.00,
        "billing_type": "annual",
        "sort_order": 50,
    },
    {
        "name": "Rediseño de Sitio Web Existente",
        "description": "Renovación completa de sitio web existente: nuevo diseño gráfico, migración de contenidos, mejoras de velocidad y SEO técnico. Mantiene la estructura de URLs para preservar posicionamiento.",
        "category": "Diseño y Desarrollo Web",
        "base_price": 900.00,
        "billing_type": "one_time",
        "sort_order": 60,
    },
    # ─── CATEGORÍA: SEO y Posicionamiento ─────────────────────────────────────
    {
        "name": "SEO Local",
        "description": "Posicionamiento en Google para palabras clave de ciudad o región específica. Incluye auditoría inicial, optimización on-page, ficha de Google Business Profile y reportes mensuales.",
        "category": "SEO y Posicionamiento",
        "base_price": 400.00,
        "billing_type": "monthly",
        "sort_order": 70,
    },
    {
        "name": "SEO Nacional",
        "description": "Estrategia SEO para posicionar en todo el país. Investigación de palabras clave con intención de compra, link building nacional, optimización técnica, creación de contenido y reportes mensuales.",
        "category": "SEO y Posicionamiento",
        "base_price": 750.00,
        "billing_type": "monthly",
        "sort_order": 80,
    },
    {
        "name": "SEO Internacional",
        "description": "Estrategia multipaís con implementación de hreflang, palabras clave por mercado, link building internacional y contenido adaptado por región. Ideal para exportadoras y SaaS.",
        "category": "SEO y Posicionamiento",
        "base_price": 1500.00,
        "billing_type": "monthly",
        "sort_order": 90,
    },
    {
        "name": "SEO para E-commerce",
        "description": "Optimización de páginas de producto, categorías y fichas técnicas. Incluye schema markup de productos, velocidad de carga, gestión de reviews y estrategia de contenido para tiendas en línea.",
        "category": "SEO y Posicionamiento",
        "base_price": 900.00,
        "billing_type": "monthly",
        "sort_order": 100,
    },
    {
        "name": "Auditoría SEO Técnica",
        "description": "Análisis completo del sitio: velocidad, Core Web Vitals, errores de rastreo, estructura de URLs, backlinks tóxicos, contenido duplicado y oportunidades de mejora. Entregable: reporte PDF ejecutivo.",
        "category": "SEO y Posicionamiento",
        "base_price": 350.00,
        "billing_type": "one_time",
        "sort_order": 110,
    },
    {
        "name": "Optimización Google Business Profile",
        "description": "Configuración y optimización completa de perfil de Google Business: fotos profesionales, categorías, horarios, reseñas, publicaciones y respuestas. Mejora visibilidad en Google Maps.",
        "category": "SEO y Posicionamiento",
        "base_price": 200.00,
        "billing_type": "one_time",
        "sort_order": 120,
    },
    # ─── CATEGORÍA: Publicidad Digital (SEM) ──────────────────────────────────
    {
        "name": "Gestión de Google Ads",
        "description": "Configuración y gestión mensual de campañas de búsqueda y display en Google Ads. Incluye estrategia, selección de palabras clave, creación de anuncios, seguimiento de conversiones y optimización semanal.",
        "category": "Publicidad Digital (SEM)",
        "base_price": 500.00,
        "billing_type": "monthly",
        "sort_order": 130,
    },
    {
        "name": "Gestión de Meta Ads (Facebook e Instagram)",
        "description": "Creación y gestión de campañas en Facebook e Instagram. Incluye segmentación de audiencias, diseño de creatividades, prueba A/B, optimización de presupuesto y reporte mensual de resultados.",
        "category": "Publicidad Digital (SEM)",
        "base_price": 450.00,
        "billing_type": "monthly",
        "sort_order": 140,
    },
    {
        "name": "Configuración Inicial de Campañas Publicitarias",
        "description": "Auditoría y configuración desde cero de cuentas Google Ads o Meta Ads: estructura de campañas, píxeles de seguimiento, públicos personalizados, conversiones y estrategia de puja.",
        "category": "Publicidad Digital (SEM)",
        "base_price": 600.00,
        "billing_type": "one_time",
        "sort_order": 150,
    },
    {
        "name": "Paquete Integral Google Ads + SEO",
        "description": "Combinación de gestión mensual de Google Ads y SEO local o nacional. Estrategia integrada de paid + organic para maximizar visibilidad y reducir costo por adquisición.",
        "category": "Publicidad Digital (SEM)",
        "base_price": 1100.00,
        "billing_type": "monthly",
        "sort_order": 160,
    },
    # ─── CATEGORÍA: Redes Sociales ─────────────────────────────────────────────
    {
        "name": "Gestión de Redes Sociales (Plan Básico)",
        "description": "Administración de 2 redes sociales (Instagram + Facebook): 12 publicaciones mensuales, diseño gráfico de contenidos, redacción de copies y respuesta a comentarios hasta 1 hora diaria.",
        "category": "Redes Sociales",
        "base_price": 350.00,
        "billing_type": "monthly",
        "sort_order": 170,
    },
    {
        "name": "Gestión de Redes Sociales (Plan Profesional)",
        "description": "Administración de 3 redes sociales (Instagram, Facebook, TikTok o LinkedIn): 20 publicaciones mensuales, diseño gráfico, reels o videos cortos, estrategia de crecimiento y reportes.",
        "category": "Redes Sociales",
        "base_price": 650.00,
        "billing_type": "monthly",
        "sort_order": 180,
    },
    {
        "name": "Estrategia de Contenido Digital",
        "description": "Desarrollo de plan editorial anual: definición de pilares de contenido, calendario mensual, guía de tono de voz, plantillas de diseño y lineamientos por red social. Entregable en 15 días hábiles.",
        "category": "Redes Sociales",
        "base_price": 500.00,
        "billing_type": "one_time",
        "sort_order": 190,
    },
    {
        "name": "Sesión Fotográfica para Redes Sociales",
        "description": "Sesión profesional de fotografía de producto, marca personal o corporativa. Incluye 2 horas de sesión, edición de hasta 40 imágenes optimizadas para uso en redes sociales y sitio web.",
        "category": "Redes Sociales",
        "base_price": 280.00,
        "billing_type": "one_time",
        "sort_order": 200,
    },
    # ─── CATEGORÍA: Inteligencia Artificial ───────────────────────────────────
    {
        "name": "Chatbot con IA para WhatsApp y Web",
        "description": "Implementación de asistente virtual con inteligencia artificial para WhatsApp Business y sitio web. Responde consultas 24/7, califica leads, agenda citas y escala a humano cuando es necesario.",
        "category": "Inteligencia Artificial",
        "base_price": 1800.00,
        "billing_type": "one_time",
        "sort_order": 210,
    },
    {
        "name": "Mantenimiento de Chatbot IA",
        "description": "Actualización mensual de flujos de conversación, entrenamiento con nuevas preguntas frecuentes, revisión de métricas de interacción, ajustes de prompts y soporte técnico del chatbot.",
        "category": "Inteligencia Artificial",
        "base_price": 200.00,
        "billing_type": "monthly",
        "sort_order": 220,
    },
    {
        "name": "Automatización de Marketing con IA",
        "description": "Configuración de flujos automáticos de captación, calificación y seguimiento de leads usando herramientas de IA. Integración con WhatsApp, email y redes sociales para nurturing multicanal.",
        "category": "Inteligencia Artificial",
        "base_price": 2200.00,
        "billing_type": "one_time",
        "sort_order": 230,
    },
    {
        "name": "Optimización para IA Search (GEO / AI SEO)",
        "description": "Posicionamiento de la marca en motores de búsqueda con IA como ChatGPT, Gemini y Perplexity. Incluye auditoría de visibilidad, optimización de contenido y estrategia de autoridad digital.",
        "category": "Inteligencia Artificial",
        "base_price": 600.00,
        "billing_type": "monthly",
        "sort_order": 240,
    },
    {
        "name": "Producción de Contenido con IA",
        "description": "Generación de imágenes, videos cortos y piezas publicitarias usando modelos de IA generativa. Paquete de 20 piezas visuales mensuales listas para usar en redes sociales y campañas.",
        "category": "Inteligencia Artificial",
        "base_price": 400.00,
        "billing_type": "monthly",
        "sort_order": 250,
    },
    {
        "name": "Consultoría de Transformación Digital con IA",
        "description": "Sesión estratégica de 4 horas con análisis de procesos de ventas, marketing y atención al cliente. Entregable: hoja de ruta de implementación de herramientas de IA adaptadas al negocio.",
        "category": "Inteligencia Artificial",
        "base_price": 800.00,
        "billing_type": "one_time",
        "sort_order": 260,
    },
    # ─── CATEGORÍA: Branding e Identidad Visual ───────────────────────────────
    {
        "name": "Diseño de Identidad de Marca (Branding Completo)",
        "description": "Creación de identidad visual corporativa: logotipo en todas sus versiones, paleta de colores, tipografías, manual de marca, papelería básica (tarjetas, membrete, firma de correo) y guía de uso.",
        "category": "Branding e Identidad Visual",
        "base_price": 950.00,
        "billing_type": "one_time",
        "sort_order": 270,
    },
    {
        "name": "Rediseño de Logo",
        "description": "Renovación de logotipo existente: modernización del diseño manteniendo reconocimiento de marca. Entrega en SVG, PNG y PDF, con 3 propuestas iniciales y 2 rondas de revisión.",
        "category": "Branding e Identidad Visual",
        "base_price": 350.00,
        "billing_type": "one_time",
        "sort_order": 280,
    },
    {
        "name": "Diseño Gráfico Mensual",
        "description": "Pack de diseño gráfico recurrente: hasta 15 piezas mensuales para redes sociales, presentaciones, flyers, banners web o materiales impresos. Entrega en formatos editables y listos para uso.",
        "category": "Branding e Identidad Visual",
        "base_price": 300.00,
        "billing_type": "monthly",
        "sort_order": 290,
    },
    # ─── CATEGORÍA: Estrategia Digital ────────────────────────────────────────
    {
        "name": "Plan de Marketing Digital 360°",
        "description": "Elaboración de estrategia digital integral: análisis de competencia, definición de buyer personas, plan de contenidos, estrategia de paid media, SEO y KPIs medibles. Entregable en 10 días hábiles.",
        "category": "Estrategia Digital",
        "base_price": 1200.00,
        "billing_type": "one_time",
        "sort_order": 300,
    },
    {
        "name": "Consultoría Mensual de Marketing Digital",
        "description": "Sesión mensual de 2 horas con especialista senior para revisar métricas, ajustar estrategia, resolver bloqueos y planificar acciones del siguiente período. Incluye acceso a dashboard de resultados.",
        "category": "Estrategia Digital",
        "base_price": 250.00,
        "billing_type": "monthly",
        "sort_order": 310,
    },
]


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        async with conn.transaction():
            inserted = 0
            current_category = None
            for svc in SERVICES:
                if svc["category"] != current_category:
                    current_category = svc["category"]
                    print(f"\n  ── {current_category} ──")

                await conn.execute(
                    """
                    INSERT INTO services (id, name, description, category, base_price,
                        billing_type, currency, is_active, sort_order)
                    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                    """,
                    uuid.uuid4(),
                    svc["name"],
                    svc["description"],
                    svc["category"],
                    svc["base_price"],
                    svc["billing_type"],
                    "USD",
                    True,
                    svc["sort_order"],
                )
                inserted += 1
                billing_label = {"one_time": "único", "monthly": "/mes", "annual": "/año"}[svc["billing_type"]]
                print(f"  [{inserted:02d}] ${svc['base_price']:>8,.2f} {billing_label:6s}  {svc['name']}")

        print(f"\n✓ {inserted} servicios insertados correctamente.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
