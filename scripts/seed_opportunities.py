"""
Seed script: 30 oportunidades vinculadas a leads y clientes existentes.
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_opportunities.py
"""
import asyncio
import uuid
from datetime import date, datetime
import asyncpg

DB_URL = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"
ADMIN_USER_ID = "d06edc36-d03f-4960-864b-e71e8baee07b"

# Probabilidad por etapa
STAGE_PROBABILITY = {
    "new":                10,
    "contacted":          25,
    "meeting_scheduled":  45,
    "diagnosis_done":     60,
    "quote_sent":         70,
    "negotiation":        82,
    "won":               100,
    "lost":                0,
}

# Oportunidades: (índice lead por full_name, índice cliente por nombre parcial,
#                 title, stage, estimated_value, expected_close_date, lost_reason)
OPPS = [
    # ── won / cerradas ganadas ──────────────────────────────────────────────
    {
        "lead":   "Alejandro Pérez Gutiérrez",
        "client": "Grupo Empresarial Alianza",
        "title":  "Implementación de CRM para equipo comercial",
        "description": "Propuesta de implementación completa del CRM para el equipo de 15 vendedores de Grupo Pérez Hermanos. Incluye módulo de pipeline, cotizaciones y reportes ejecutivos.",
        "stage":  "won",
        "value":  3800.00,
        "close":  date(2026, 5, 20),
        "closed_at": datetime(2026, 5, 20, 14, 30),
        "lost_reason": None,
    },
    {
        "lead":   "Roberto Alonso Jiménez Brenes",
        "client": "Logística Express Centroamérica",
        "title":  "CRM multipaís para importadora JB del Caribe",
        "description": "Solución CRM para gestión de clientes en 3 países. Incluye módulo de leads, oportunidades y cotizaciones en USD. Integración con equipo de ventas regional.",
        "stage":  "won",
        "value":  5200.00,
        "close":  date(2026, 4, 30),
        "closed_at": datetime(2026, 4, 30, 10, 0),
        "lost_reason": None,
    },
    {
        "lead":   "Diego Mauricio Guzmán Pérez",
        "client": "Tecnología Digital Latina S.R.L.",
        "title":  "Integración CRM + ERP para Tech Solutions Guzmán",
        "description": "Proyecto de integración del CRM con sistema ERP existente vía API REST. Pipeline de oportunidades, seguimiento de tickets y reportes unificados para empresa de TI.",
        "stage":  "won",
        "value":  6500.00,
        "close":  date(2026, 5, 10),
        "closed_at": datetime(2026, 5, 10, 16, 0),
        "lost_reason": None,
    },
    # ── lost / cerradas perdidas ────────────────────────────────────────────
    {
        "lead":   "Eduardo Rafael Vega Mora",
        "client": "Distribuidora El Mercado Tropical",
        "title":  "Sistema de control de flota y clientes Vega Express",
        "description": "Propuesta para digitalizar el control de rutas y clientes corporativos de empresa de transporte. No avanzó por restricciones presupuestarias del cliente.",
        "stage":  "lost",
        "value":  2200.00,
        "close":  date(2026, 4, 15),
        "closed_at": datetime(2026, 4, 15, 9, 0),
        "lost_reason": "El cliente decidió contratar una solución más económica con funcionalidad limitada. Prioridad de reducción de costos por reestructuración interna.",
    },
    {
        "lead":   "Adriana Marcela Núñez Barrantes",
        "client": "Medios y Comunicaciones Caribe S.A.",
        "title":  "Control de pedidos VIP para Joyería Artesanal Núñez",
        "description": "Propuesta de módulo de clientes y pedidos personalizados para joyería artesanal. El ticket fue pequeño y el cliente no tenía presupuesto suficiente.",
        "stage":  "lost",
        "value":  850.00,
        "close":  date(2026, 5, 5),
        "closed_at": datetime(2026, 5, 5, 11, 0),
        "lost_reason": "Presupuesto insuficiente. El cliente consideró que el costo mensual no se justificaba para el tamaño de su operación actual.",
    },
    # ── negotiation ─────────────────────────────────────────────────────────
    {
        "lead":   "Arturo Sebastián Brenes Acosta",
        "client": "Importadora Pacífico Norte S.A.",
        "title":  "CRM regional para Brenes Logística Internacional",
        "description": "Implementación de CRM para empresa logística con operaciones en CR, PAN y COL. Módulos de clientes, oportunidades, cotizaciones multimoneda y reportes consolidados.",
        "stage":  "negotiation",
        "value":  7800.00,
        "close":  date(2026, 7, 15),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Ernesto Guillermo Picado Mora",
        "client": "Bufete Jurídico Sánchez & Asociados",
        "title":  "Gestión de contratos y clientes para Seguridad Fortis",
        "description": "CRM para empresa de seguridad privada con 60 guardas. Control de contratos con clientes corporativos, renovaciones, facturación recurrente y seguimiento de SLA.",
        "stage":  "negotiation",
        "value":  4500.00,
        "close":  date(2026, 7, 31),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Alberto Enrique Mora Badilla",
        "client": "Soluciones Financieras del Sur Ltda.",
        "title":  "CRM financiero con cartera de 800 clientes activos",
        "description": "Plataforma CRM adaptada para financiera: seguimiento de prospectos, gestión de cartera, alertas de vencimiento, reportes de captación y retención de clientes.",
        "stage":  "negotiation",
        "value":  9200.00,
        "close":  date(2026, 8, 15),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "José Ángel Bermúdez Vega",
        "client": "Clínica de Salud Integral Bienestar",
        "title":  "CRM de ventas para distribuidora de equipos médicos",
        "description": "Pipeline de ventas para distribución de equipos médicos a clínicas y hospitales. Módulo de cotizaciones con catálogo técnico, seguimiento post-venta y soporte.",
        "stage":  "negotiation",
        "value":  5800.00,
        "close":  date(2026, 7, 20),
        "closed_at": None,
        "lost_reason": None,
    },
    # ── quote_sent ──────────────────────────────────────────────────────────
    {
        "lead":   "Jorge Luis Campos Benavides",
        "client": "Desarrolladora Residencial Palmares",
        "title":  "CRM inmobiliario para Agencia Campos — pipeline de propiedades",
        "description": "Solución CRM para agencia inmobiliaria con 10 asesores. Pipeline de propiedades disponibles, seguimiento de prospectos compradores, historial de visitas y cotizaciones.",
        "stage":  "quote_sent",
        "value":  4200.00,
        "close":  date(2026, 7, 10),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Lorena Beatriz Arias Méndez",
        "client": "Servicios Ambientales GreenTech S.A.",
        "title":  "Gestión de proyectos y cotizaciones para Arias & Méndez Arq.",
        "description": "CRM para firma de arquitectos: control de proyectos en curso, cotizaciones por etapa, seguimiento de clientes y generación de reportes de avance para cada proyecto.",
        "stage":  "quote_sent",
        "value":  3100.00,
        "close":  date(2026, 7, 5),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Manuel Antonio Quesada Ulate",
        "client": "Exportaciones Café Verde S.A.",
        "title":  "CRM agro-exportador para Agrícola Los Naranjos",
        "description": "Sistema CRM para gestión de compradores internacionales de piña. Seguimiento de pedidos, historial de exportaciones por cliente, cumplimiento de contratos y trazabilidad.",
        "stage":  "quote_sent",
        "value":  4800.00,
        "close":  date(2026, 7, 25),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Isabel Lucía Ulate Fonseca",
        "client": "Distribuidora El Mercado Tropical",
        "title":  "Gestión de pedidos B2B para Textiles Ulate & Moda",
        "description": "Módulo de pedidos B2B para empresa textil que vende a tiendas y boutiques. Control de órdenes de compra, historial por cliente, crédito otorgado y seguimiento de entregas.",
        "stage":  "quote_sent",
        "value":  3500.00,
        "close":  date(2026, 8, 5),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Ricardo Antonio Gamboa Vindas",
        "client": "Constructora Los Pinos S.A.",
        "title":  "Control de licitaciones y propuestas — Gamboa Ingeniería",
        "description": "CRM para ingeniería civil: pipeline de licitaciones públicas y privadas, seguimiento de propuestas, gestión de subcontratistas y control de etapas de proyecto por cliente.",
        "stage":  "quote_sent",
        "value":  5500.00,
        "close":  date(2026, 8, 1),
        "closed_at": None,
        "lost_reason": None,
    },
    # ── diagnosis_done ──────────────────────────────────────────────────────
    {
        "lead":   "Ana Patricia Salas Ureña",
        "client": "Bufete Jurídico Sánchez & Asociados",
        "title":  "Seguimiento de clientes para Asesoría Contable Salas",
        "description": "Herramienta CRM para firma contable: módulo de tareas, recordatorios por cliente, historial de reuniones y documentos, y seguimiento de vencimientos fiscales.",
        "stage":  "diagnosis_done",
        "value":  1800.00,
        "close":  date(2026, 8, 20),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Mariela Gabriela Prado Arce",
        "client": "Instituto Educativo Latinoamérica",
        "title":  "Módulo de admisiones para Centro Educativo Bilingüe Prado",
        "description": "Sistema de seguimiento del proceso de admisiones: desde primer contacto de familias hasta matrícula. Automatización de comunicaciones, documentos requeridos y estadísticas.",
        "stage":  "diagnosis_done",
        "value":  4100.00,
        "close":  date(2026, 8, 30),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Gustavo Adolfo Ramírez Solano",
        "client": "Constructora Los Pinos S.A.",
        "title":  "CRM de clientes y cotizaciones para Ferretería Ramírez",
        "description": "Módulo de gestión de clientes constructoras para ferretería industrial. Catálogo de productos, generación de cotizaciones, crédito por cliente y seguimiento de pedidos.",
        "stage":  "diagnosis_done",
        "value":  2800.00,
        "close":  date(2026, 9, 10),
        "closed_at": None,
        "lost_reason": None,
    },
    # ── meeting_scheduled ───────────────────────────────────────────────────
    {
        "lead":   "María Isabel Rodríguez Fallas",
        "client": "Grupo Empresarial Alianza S.A.",
        "title":  "Módulo de cotizaciones para Comercializadora Rodríguez e Hijos",
        "description": "Implementación del módulo de cotizaciones y facturación para distribuidora con 8 vendedores. Flujo: lead → oportunidad → cotización → aprobación → factura.",
        "stage":  "meeting_scheduled",
        "value":  3200.00,
        "close":  date(2026, 9, 15),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Silvia Estela Mora Portuguez",
        "client": "Clínica de Salud Integral Bienestar",
        "title":  "Agenda y seguimiento de pacientes — Clínica Dental Mora",
        "description": "CRM adaptado para clínica dental: módulo de citas, historial clínico por paciente, seguimiento de tratamientos de ortodoncia, cobros y recordatorios automáticos.",
        "stage":  "meeting_scheduled",
        "value":  2600.00,
        "close":  date(2026, 9, 20),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Rebeca Tatiana Blanco Vásquez",
        "client": "Bufete Jurídico Sánchez & Asociados",
        "title":  "Pipeline comercial para firma de RRHH Blanco & Partners",
        "description": "Herramienta de seguimiento de clientes empresariales para firma de recursos humanos. Módulo de propuestas, contratos, seguimiento de proyectos de selección y reportes.",
        "stage":  "meeting_scheduled",
        "value":  2400.00,
        "close":  date(2026, 9, 30),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Yolanda Esperanza Ruiz Pérez",
        "client": "Servicios Ambientales GreenTech S.A.",
        "title":  "Gestión de contratos de limpieza — Servicios Ruiz S.A.",
        "description": "CRM para empresa de limpieza con 40 empleados: control de contratos por cliente corporativo, facturación recurrente, alertas de renovación y seguimiento de calidad.",
        "stage":  "meeting_scheduled",
        "value":  3000.00,
        "close":  date(2026, 10, 1),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Sebastián Andrés Torres Chacón",
        "client": "Agencia Creativa Fusión Digital",
        "title":  "Automatización de prospectos para Media Digital Torres",
        "description": "CRM para agencia de marketing digital: pipeline de prospectos, seguimiento de propuestas, control de proyectos activos, facturación mensual y reportes de rentabilidad.",
        "stage":  "meeting_scheduled",
        "value":  2900.00,
        "close":  date(2026, 10, 5),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Priscila Marcela Aguilar Calvo",
        "client": "Agencia Creativa Fusión Digital",
        "title":  "Seguimiento de clientes para Marketing de Contenidos Praxis",
        "description": "Herramienta de seguimiento para agencia de contenidos con 15 clientes activos. Automatización de reportes mensuales, control de entregables y renovaciones de contrato.",
        "stage":  "meeting_scheduled",
        "value":  2200.00,
        "close":  date(2026, 10, 10),
        "closed_at": None,
        "lost_reason": None,
    },
    # ── contacted ───────────────────────────────────────────────────────────
    {
        "lead":   "Verónica Liliana Herrera Picado",
        "client": "Distribuidora El Mercado Tropical",
        "title":  "Sistema de ventas con WhatsApp para Distribuciones VH",
        "description": "Módulo de seguimiento de vendedoras con integración de WhatsApp para empresa de productos de belleza. Control de pedidos, comisiones y cartera de clientas por zona.",
        "stage":  "contacted",
        "value":  1900.00,
        "close":  date(2026, 10, 20),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Marco Antonio Valverde Hidalgo",
        "client": "Cooperativa Agrícola del Valle Central",
        "title":  "Digitalización de pedidos corporativos — El Trigo Dorado",
        "description": "Sistema de gestión de pedidos para panadería con 3 sucursales. Control de clientes corporativos, pedidos por encargo, facturación y estadísticas de ventas por punto.",
        "stage":  "contacted",
        "value":  2100.00,
        "close":  date(2026, 11, 1),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Gloria Patricia Leiva Sandoval",
        "client": "Clínica de Salud Integral Bienestar",
        "title":  "Gestión de pacientes para Centro Terapéutico Mente Sana",
        "description": "CRM para centro de psicología: agendamiento de citas, historial de sesiones por paciente, seguimiento terapéutico, recordatorios y control de pagos.",
        "stage":  "contacted",
        "value":  1700.00,
        "close":  date(2026, 11, 10),
        "closed_at": None,
        "lost_reason": None,
    },
    # ── new ─────────────────────────────────────────────────────────────────
    {
        "lead":   "Carlos Enrique Mora Vindas",
        "client": "Grupo Empresarial Alianza S.A.",
        "title":  "Pipeline de ventas para Servicios Integrales Mora S.R.L.",
        "description": "Implementación de CRM con pipeline visual para equipo de 5 comerciales. Módulos de leads, oportunidades, tareas y reportes de avance semanal.",
        "stage":  "new",
        "value":  2500.00,
        "close":  date(2026, 11, 30),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Fernando José Cascante Alfaro",
        "client": "Constructora Los Pinos S.A.",
        "title":  "CRM de proyectos para Construcciones Cascante S.A.",
        "description": "Sistema de gestión de clientes y proyectos para constructora mediana. Control de etapas de obra, contratos, cotizaciones y clientes empresariales e institucionales.",
        "stage":  "new",
        "value":  3300.00,
        "close":  date(2026, 12, 15),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Natalia Cristina Murillo Zamora",
        "client": "Hotel & Spa Las Brisas del Atlántico",
        "title":  "Cotizaciones y seguimiento de eventos para Murillo Producciones",
        "description": "Módulo de gestión de eventos corporativos y bodas: formulario de requerimientos, cotización rápida, seguimiento de contratos y control de pagos por etapa.",
        "stage":  "new",
        "value":  2700.00,
        "close":  date(2026, 12, 20),
        "closed_at": None,
        "lost_reason": None,
    },
    {
        "lead":   "Luisa Fernanda Vargas Solano",
        "client": "Farmacéutica Nacional Salud Total",
        "title":  "Analítica de ventas para Consultora LF Vargas & Co.",
        "description": "Módulo de reportes y analítica comercial para consultora independiente. Dashboards de cartera, actividades por cliente, proyección de ingresos y KPIs de gestión.",
        "stage":  "new",
        "value":  1500.00,
        "close":  date(2027, 1, 15),
        "closed_at": None,
        "lost_reason": None,
    },
]


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # Cargar leads indexados por full_name
        lead_rows = await conn.fetch("SELECT id, full_name FROM leads")
        leads_by_name = {r["full_name"]: r["id"] for r in lead_rows}

        # Cargar clientes con su contacto primario
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) AS contact_id
            FROM clients c
        """)
        clients_by_name = {}
        for r in client_rows:
            clients_by_name[r["name"]] = {"id": r["id"], "contact_id": r["contact_id"]}

        def find_client(partial_name):
            for name, data in clients_by_name.items():
                if partial_name.lower() in name.lower():
                    return name, data
            raise ValueError(f"Cliente no encontrado: {partial_name!r}")

        async with conn.transaction():
            inserted = 0
            current_stage = None
            for opp in OPPS:
                lead_id = leads_by_name.get(opp["lead"])
                if not lead_id:
                    print(f"  ⚠ Lead no encontrado: {opp['lead']}")
                    continue

                client_name, client_data = find_client(opp["client"])
                client_id = client_data["id"]
                contact_id = client_data["contact_id"]

                stage = opp["stage"]
                probability = STAGE_PROBABILITY[stage]

                if stage != current_stage:
                    current_stage = stage
                    labels = {
                        "won": "GANADAS", "lost": "PERDIDAS", "negotiation": "NEGOCIACIÓN",
                        "quote_sent": "COTIZACIÓN ENVIADA", "diagnosis_done": "DIAGNÓSTICO HECHO",
                        "meeting_scheduled": "REUNIÓN AGENDADA", "contacted": "CONTACTADOS", "new": "NUEVAS",
                    }
                    print(f"\n  ── {labels.get(stage, stage.upper())} ──")

                await conn.execute(
                    """
                    INSERT INTO opportunities (
                        id, client_id, contact_id, lead_id, title, description,
                        stage, estimated_value, probability, expected_close_date,
                        closed_at, owner_user_id, lost_reason
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
                    """,
                    uuid.uuid4(),
                    client_id,
                    contact_id,
                    lead_id,
                    opp["title"],
                    opp["description"],
                    stage,
                    opp["value"],
                    probability,
                    opp["close"],
                    opp.get("closed_at"),
                    uuid.UUID(ADMIN_USER_ID),
                    opp.get("lost_reason"),
                )
                inserted += 1
                closed_tag = " ✓" if stage == "won" else (" ✗" if stage == "lost" else "")
                print(f"  [{inserted:02d}] ${opp['value']:>8,.2f} | {probability:3d}% | {opp['title'][:60]}{closed_tag}")

        print(f"\n✓ {inserted} oportunidades insertadas correctamente.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
