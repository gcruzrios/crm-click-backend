"""
Seed script: rellena el pipeline con oportunidades para clientes sin cobertura
y segunda oportunidad en clientes clave. Distribuye todas las etapas equitativamente.
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_pipeline_fill.py
"""
import asyncio
import uuid
from datetime import date, datetime
import asyncpg

DB_URL   = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"
ADMIN_ID = "d06edc36-d03f-4960-864b-e71e8baee07b"

STAGE_PROB = {
    "new": 10, "contacted": 25, "meeting_scheduled": 45,
    "diagnosis_done": 60, "quote_sent": 70, "negotiation": 82,
    "won": 100, "lost": 0,
}

# (client_partial, title, description, stage, value, close_date, closed_at, lost_reason)
NEW_OPPS = [
    # ── NUEVAS (new) ──────────────────────────────────────────────────────────
    {
        "client": "Bufete Jurídico Sánchez",
        "title": "Digitalización de expedientes y CRM jurídico — Bufete Sánchez",
        "description": "Plataforma CRM para gestión de expedientes legales por cliente: historial de casos, vencimientos judiciales, asignación de abogados, cotizaciones de honorarios y facturación.",
        "stage": "new", "value": 4500.00,
        "close": date(2027, 1, 15), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Importadora Pacífico Norte",
        "title": "CRM de inventario y clientes — Importadora Pacífico Norte",
        "description": "Sistema CRM integrado con módulo de inventario para importadora. Gestión de proveedores internacionales, órdenes de compra, clientes distribuidores y seguimiento de embarques.",
        "stage": "new", "value": 6200.00,
        "close": date(2027, 1, 30), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Inversiones Centroamérica Holdings",
        "title": "CRM corporativo multiempresa — ICA Holdings Guatemala",
        "description": "CRM corporativo para grupo de inversiones con subsidiarias en 4 países. Módulo de prospectos institucionales, gestión de portafolio de clientes y reportes consolidados por empresa.",
        "stage": "new", "value": 12000.00,
        "close": date(2027, 2, 15), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Grupo Empresarial Alianza",
        "title": "Módulo de inteligencia comercial y BI — Grupo Alianza",
        "description": "Segunda fase del CRM: módulo de business intelligence con dashboards ejecutivos, análisis de cartera de clientes, proyección de ingresos y alertas de riesgo de pérdida.",
        "stage": "new", "value": 7500.00,
        "close": date(2027, 1, 10), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Supermercados La Colonia del Este",
        "title": "CRM de proveedores y negociaciones — La Colonia del Este",
        "description": "Módulo de gestión de proveedores para cadena de supermercados: negociación de contratos, historial de condiciones comerciales, evaluación de desempeño y alertas de vencimiento.",
        "stage": "new", "value": 8900.00,
        "close": date(2027, 2, 28), "closed_at": None, "lost_reason": None,
    },
    # ── CONTACTADOS (contacted) ───────────────────────────────────────────────
    {
        "client": "Instituto Educativo Latinoamérica",
        "title": "Módulo de matrícula y seguimiento académico — Instituto LA",
        "description": "CRM educativo para gestión del proceso de matrícula de 3,500 estudiantes: seguimiento de renovaciones, comunicaciones automáticas a familias, reporte de deserción y alertas de riesgo.",
        "stage": "contacted", "value": 5400.00,
        "close": date(2026, 11, 30), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Clínica de Salud Integral Bienestar",
        "title": "CRM de referencias médicas entre especialidades — Clínica Bienestar",
        "description": "Módulo de referencias internas entre las 12 especialidades de la clínica. Seguimiento del recorrido del paciente, historial de consultas, indicadores de satisfacción y reportes médicos.",
        "stage": "contacted", "value": 3800.00,
        "close": date(2026, 12, 1), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Medios y Comunicaciones Caribe",
        "title": "Pipeline comercial para venta de pauta publicitaria — Medios Caribe",
        "description": "CRM para el equipo de ventas de publicidad: seguimiento de anunciantes, propuestas de pauta en radio y TV, contratos, control de facturación mensual y métricas de audiencia por cliente.",
        "stage": "contacted", "value": 5800.00,
        "close": date(2026, 12, 10), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Logística Express Centroamérica",
        "title": "Módulo de clientes corporativos y contratos — Logística Express",
        "description": "Segunda fase CRM: módulo de contratos de servicio logístico por cliente, SLAs por ruta, alertas de incumplimiento, facturación recurrente y reportes de desempeño mensual.",
        "stage": "contacted", "value": 4700.00,
        "close": date(2026, 12, 15), "closed_at": None, "lost_reason": None,
    },
    # ── REUNIÓN AGENDADA (meeting_scheduled) ──────────────────────────────────
    {
        "client": "Tecnología Digital Latina",
        "title": "Plataforma de soporte y tickets para clientes — TecDigital",
        "description": "Módulo CRM de helpdesk: gestión de tickets de soporte por cliente, SLAs, asignación a técnicos, historial de incidencias, encuestas de satisfacción y reportes de calidad.",
        "stage": "meeting_scheduled", "value": 4600.00,
        "close": date(2026, 10, 25), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Distribuidora El Mercado Tropical",
        "title": "Reactivación CRM tras reestructuración — Mercado Tropical",
        "description": "Retoma de proyecto CRM post-reestructuración interna. Módulo de cartera de clientes distribuidores, historial de pedidos, crédito comercial y seguimiento de cobranza.",
        "stage": "meeting_scheduled", "value": 4200.00,
        "close": date(2026, 11, 5), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Bufete Jurídico Sánchez",
        "title": "Portal de clientes y gestión de honorarios — Bufete Sánchez",
        "description": "Portal self-service para clientes del bufete: consulta de estado de casos, documentos compartidos, aprobación de honorarios en línea y historial de pagos. Segunda fase del CRM jurídico.",
        "stage": "meeting_scheduled", "value": 3200.00,
        "close": date(2026, 11, 20), "closed_at": None, "lost_reason": None,
    },
    # ── DIAGNÓSTICO HECHO (diagnosis_done) ────────────────────────────────────
    {
        "client": "Servicios Ambientales GreenTech",
        "title": "CRM de proyectos ISO y clientes ambientales — GreenTech",
        "description": "CRM para firma ambiental: pipeline de licitaciones de consultoría ISO 14001, seguimiento de proyectos de gestión de residuos, clientes corporativos y reporte de impacto ambiental.",
        "stage": "diagnosis_done", "value": 3900.00,
        "close": date(2026, 10, 1), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Inversiones Centroamérica Holdings",
        "title": "Módulo de due diligence y prospección — ICA Holdings",
        "description": "Segunda fase: módulo de due diligence para evaluación de empresas objetivo. Pipeline de adquisiciones, documentación por empresa analizada, alertas de hitos y reportes a junta directiva.",
        "stage": "diagnosis_done", "value": 9500.00,
        "close": date(2026, 10, 20), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Supermercados La Colonia del Este",
        "title": "CRM de fidelización y tarjeta de puntos — La Colonia del Este",
        "description": "Plataforma de fidelización de clientes para cadena de supermercados: programa de puntos, segmentación de clientes VIP, promociones personalizadas y analítica de comportamiento de compra.",
        "stage": "diagnosis_done", "value": 9200.00,
        "close": date(2026, 10, 30), "closed_at": None, "lost_reason": None,
    },
    # ── COTIZACIÓN ENVIADA (quote_sent) ───────────────────────────────────────
    {
        "client": "Hotel & Spa Las Brisas",
        "title": "Sistema de grupos corporativos y spa — Hotel Brisas del Atlántico",
        "description": "CRM para gestión de reservas grupales y servicios spa: cotización de paquetes all-inclusive, seguimiento de depósitos, planificación de eventos y reportes de ocupación por segmento.",
        "stage": "quote_sent", "value": 5100.00,
        "close": date(2026, 8, 25), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Tecnología Digital Latina",
        "title": "CRM integrado con facturación electrónica — TecDigital Latina",
        "description": "Integración del CRM con sistema de facturación electrónica para empresa de tecnología. Automatización del flujo cotización → aprobación → factura electrónica → pago → cierre.",
        "stage": "quote_sent", "value": 5900.00,
        "close": date(2026, 9, 5), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Importadora Pacífico Norte",
        "title": "Automatización de cotizaciones de importación — Pacífico Norte",
        "description": "Módulo de cotizaciones automáticas para importadora: cálculo de costos de importación (CIF, aranceles, IVA), generación de proformas en USD y seguimiento de aprobación del cliente.",
        "stage": "quote_sent", "value": 4100.00,
        "close": date(2026, 9, 10), "closed_at": None, "lost_reason": None,
    },
    # ── NEGOCIACIÓN (negotiation) ─────────────────────────────────────────────
    {
        "client": "Soluciones Financieras del Sur",
        "title": "CRM de expansión centroamericana — Soluciones Financieras Sur",
        "description": "Plataforma CRM para soporte a la expansión regional de empresa colombiana en CR, PAN y GT. Gestión unificada de prospectos corporativos, pipeline de captación y reportes por mercado.",
        "stage": "negotiation", "value": 11500.00,
        "close": date(2026, 9, 15), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Medios y Comunicaciones Caribe",
        "title": "Plataforma digital de ventas publicitarias — Medios Caribe",
        "description": "Segunda negociación tras reactivación del presupuesto: plataforma completa de ventas de pauta con CRM, propuestas automatizadas, seguimiento de campañas activas y reportes de efectividad.",
        "stage": "negotiation", "value": 7300.00,
        "close": date(2026, 9, 30), "closed_at": None, "lost_reason": None,
    },
    {
        "client": "Logística Express Centroamérica",
        "title": "CRM con rastreo de entregas en tiempo real — Logística Express",
        "description": "Módulo de rastreo de entregas integrado al CRM: actualización de estado por WhatsApp al cliente, alertas de demora, gestión de reclamos, historial de envíos y métricas de puntualidad.",
        "stage": "negotiation", "value": 8600.00,
        "close": date(2026, 10, 5), "closed_at": None, "lost_reason": None,
    },
    # ── GANADAS (won) ─────────────────────────────────────────────────────────
    {
        "client": "Logística Express Centroamérica",
        "title": "Implementación inicial CRM — Logística Express CA",
        "description": "Primera fase de implementación del CRM para empresa logística: módulo de clientes corporativos, oportunidades de nuevas rutas, cotizaciones de servicio y seguimiento post-venta.",
        "stage": "won", "value": 6800.00,
        "close": date(2026, 3, 15), "closed_at": datetime(2026, 3, 15, 15, 0),
        "lost_reason": None,
    },
    {
        "client": "Constructora Los Pinos",
        "title": "CRM de subcontratistas y proveedores — Constructora Los Pinos",
        "description": "Módulo de gestión de subcontratistas integrado: base de datos de proveedores calificados, órdenes de servicio por proyecto, evaluación de desempeño y control de pagos pendientes.",
        "stage": "won", "value": 3600.00,
        "close": date(2026, 4, 20), "closed_at": datetime(2026, 4, 20, 10, 30),
        "lost_reason": None,
    },
    {
        "client": "Instituto Educativo Latinoamérica",
        "title": "Sistema de gestión de convenios — Instituto Latinoamérica",
        "description": "Módulo de gestión de convenios institucionales: seguimiento de alianzas con empresas para práctica profesional, becas corporativas, historial de contactos y renovaciones anuales.",
        "stage": "won", "value": 4300.00,
        "close": date(2026, 5, 5), "closed_at": datetime(2026, 5, 5, 14, 0),
        "lost_reason": None,
    },
    # ── PERDIDAS (lost) ───────────────────────────────────────────────────────
    {
        "client": "Distribuidora El Mercado Tropical",
        "title": "CRM de distribución y pedidos B2B — Mercado Tropical",
        "description": "Propuesta de sistema CRM para distribuidora: gestión de cartera de clientes minoristas, pedidos automatizados, crédito comercial y seguimiento de cobranza. No se cerró por fusión.",
        "stage": "lost", "value": 4200.00,
        "close": date(2026, 3, 1), "closed_at": datetime(2026, 3, 1, 9, 0),
        "lost_reason": "Empresa en proceso de fusión con otro distribuidor. Congelaron todos los proyectos de TI hasta definir la nueva estructura organizacional. Retomar contacto en Q4 2026.",
    },
    {
        "client": "Supermercados La Colonia del Este",
        "title": "Plataforma de lealtad multicanal — La Colonia del Este",
        "description": "Propuesta para plataforma de lealtad omnicanal: app móvil, tarjeta física, puntos en línea y en tienda, segmentación de clientes y promociones personalizadas por perfil de compra.",
        "stage": "lost", "value": 15500.00,
        "close": date(2026, 5, 1), "closed_at": datetime(2026, 5, 1, 11, 0),
        "lost_reason": "Proceso de adquisición por cadena internacional. El comprador tiene plataforma propia de fidelización y no contempla adoptar sistemas locales en el corto plazo.",
    },
    {
        "client": "Soluciones Financieras del Sur",
        "title": "Piloto CRM Colombia — Soluciones Financieras del Sur",
        "description": "Propuesta de piloto de CRM para operación Colombia antes de expansión centroamericana. Se perdió ante solución local con mejor integración con banca colombiana.",
        "stage": "lost", "value": 8200.00,
        "close": date(2026, 4, 10), "closed_at": datetime(2026, 4, 10, 16, 0),
        "lost_reason": "El cliente priorizó una solución local colombiana con integraciones nativas con las principales entidades financieras del país. Retomar para la fase de expansión CR-PAN.",
    },
    {
        "client": "Servicios Ambientales GreenTech",
        "title": "CRM piloto para división de auditorías — GreenTech S.A.",
        "description": "Propuesta de piloto CRM para división de auditorías ambientales. No avanzó por cambio en prioridades estratégicas de la empresa hacia proyectos de energía renovable.",
        "stage": "lost", "value": 2900.00,
        "close": date(2026, 5, 20), "closed_at": datetime(2026, 5, 20, 10, 0),
        "lost_reason": "La empresa reorientó su inversión hacia una nueva división de energía renovable. El proyecto CRM quedó fuera del presupuesto aprobado para 2026.",
    },
]


STAGE_ORDER = ["new", "contacted", "meeting_scheduled", "diagnosis_done",
               "quote_sent", "negotiation", "won", "lost"]

STAGE_LABELS = {
    "new": "NUEVA", "contacted": "CONTACTADO", "meeting_scheduled": "REUNIÓN AGENDADA",
    "diagnosis_done": "DIAGNÓSTICO", "quote_sent": "COTIZACIÓN ENVIADA",
    "negotiation": "NEGOCIACIÓN", "won": "GANADA ✓", "lost": "PERDIDA ✗",
}


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # Cargar clientes con su contacto primario
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct
                    WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) AS contact_id
            FROM clients c
        """)
        clients_idx = {r["name"]: {"id": r["id"], "contact_id": r["contact_id"]} for r in client_rows}

        def find_client(partial):
            for name, data in clients_idx.items():
                if partial.lower() in name.lower():
                    return name, data
            raise ValueError(f"Cliente no encontrado: {partial!r}")

        inserted = 0
        current_stage = None

        async with conn.transaction():
            for item in NEW_OPPS:
                client_name, client_data = find_client(item["client"])

                stage = item["stage"]
                if stage != current_stage:
                    current_stage = stage
                    print(f"\n  ── {STAGE_LABELS[stage]} ──")

                await conn.execute("""
                    INSERT INTO opportunities (
                        id, client_id, contact_id, lead_id, title, description,
                        stage, estimated_value, probability, expected_close_date,
                        closed_at, owner_user_id, lost_reason
                    ) VALUES ($1,$2,$3,NULL,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                """,
                    uuid.uuid4(),
                    client_data["id"], client_data["contact_id"],
                    item["title"], item["description"],
                    stage, item["value"], STAGE_PROB[stage],
                    item["close"], item.get("closed_at"),
                    uuid.UUID(ADMIN_ID), item.get("lost_reason"),
                )
                inserted += 1
                print(f"  [{inserted:02d}] ${item['value']:>9,.2f}   {client_name}")

        # Resumen final
        stats = await conn.fetch("""
            SELECT stage, COUNT(*) as n, SUM(estimated_value) as total
            FROM opportunities GROUP BY stage
        """)
        stats_map = {r["stage"]: r for r in stats}

        total_n = await conn.fetchval("SELECT COUNT(*) FROM opportunities")
        total_v = await conn.fetchval("SELECT SUM(estimated_value) FROM opportunities")

        print(f"\n{'═'*62}")
        print(f"  {'ETAPA':24s} {'#':>4}  {'VALOR TOTAL':>14}  {'PROB':>4}")
        print(f"{'─'*62}")
        for s in STAGE_ORDER:
            if s in stats_map:
                r = stats_map[s]
                bar = "█" * r["n"]
                print(f"  {STAGE_LABELS[s]:24s} {r['n']:>4}  ${float(r['total']):>12,.2f}  {STAGE_PROB[s]:>3}%  {bar}")
        print(f"{'─'*62}")
        print(f"  {'TOTAL PIPELINE':24s} {total_n:>4}  ${float(total_v):>12,.2f}")
        print(f"{'═'*62}")
        print(f"\n✓ {inserted} oportunidades nuevas agregadas al pipeline.")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
