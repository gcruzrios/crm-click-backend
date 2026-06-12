"""
Seed script: 20 tareas del CRM vinculadas a leads, clientes y oportunidades.
  - status: pending(8) | in_progress(5) | completed(5) | cancelled(2)
  - priority: high(7) | medium(9) | low(4)
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_tasks.py
"""
import asyncio
import uuid
from datetime import datetime
import asyncpg

DB_URL   = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"
ADMIN_ID = "d06edc36-d03f-4960-864b-e71e8baee07b"

# ─── Definición de 20 tareas ─────────────────────────────────────────────────
# Cada tarea: title, description, status, priority, due_date, completed_at,
#             client(partial|None), lead(full_name|None), opp_client(partial|None)
# ─────────────────────────────────────────────────────────────────────────────
TASKS = [

    # ══ PENDING — alta prioridad ═════════════════════════════════════════════
    {
        "title": "Llamada de cierre con Finanzas y Crédito Mora",
        "description": (
            "Realizar llamada de negociación final con Alberto Enrique Mora para cerrar "
            "contrato de CRM financiero. Revisar propuesta de $9,200 en negociación. "
            "Preparar argumentos sobre ROI y reducción de tiempo de gestión de cartera."
        ),
        "status": "pending", "priority": "high",
        "due_date": datetime(2026, 6, 13, 10, 0),
        "completed_at": None,
        "client": "Finanzas y Crédito Mora",
        "lead": "Alberto Enrique Mora Badilla",
        "opp_client": "Finanzas y Crédito Mora",
    },
    {
        "title": "Preparar demo personalizada para Tech Solutions Guzmán",
        "description": (
            "Configurar ambiente de demostración con datos de empresa de TI. "
            "Mostrar integración CRM + ERP vía API REST y módulo de pipeline de ventas. "
            "Incluir caso de éxito de empresa tecnológica similar. Contacto: Diego Guzmán."
        ),
        "status": "pending", "priority": "high",
        "due_date": datetime(2026, 6, 16, 9, 0),
        "completed_at": None,
        "client": "Tech Solutions Guzmán",
        "lead": "Diego Mauricio Guzmán Pérez",
        "opp_client": "Tech Solutions Guzmán",
    },
    {
        "title": "Enviar cotización revisada a Clínica Dental Mora",
        "description": (
            "Actualizar COT-2026-016 con módulo de recordatorios automáticos de citas vía "
            "WhatsApp solicitado por Dra. Silvia Mora. Ajustar precio unitario del servicio "
            "de Meta Ads y reenviar antes del vencimiento del 1 de agosto."
        ),
        "status": "pending", "priority": "high",
        "due_date": datetime(2026, 6, 14, 16, 0),
        "completed_at": None,
        "client": "Clínica Dental Mora",
        "lead": "Silvia Estela Mora Portuguez",
        "opp_client": "Clínica Dental Mora",
    },
    {
        "title": "Preparar propuesta técnica para Brenes Logística Internacional",
        "description": (
            "Elaborar propuesta detallada para CRM multipaís CR-PAN-COL con arquitectura "
            "técnica, cronograma de implementación por fases y plan de capacitación. "
            "Incluir cláusula de soporte bilingüe. Presentar a Arturo Brenes el 20 jun."
        ),
        "status": "pending", "priority": "high",
        "due_date": datetime(2026, 6, 19, 12, 0),
        "completed_at": None,
        "client": "Brenes Logística Internacional",
        "lead": "Arturo Sebastián Brenes Acosta",
        "opp_client": "Brenes Logística Internacional",
    },
    {
        "title": "Presentación para licitación pública — Farmacéutica Salud Total",
        "description": (
            "Preparar deck ejecutivo de 15 diapositivas para presentar en proceso de "
            "licitación pública de Farmacéutica Nacional Salud Total en julio 2026. "
            "Incluir: funcionalidades de visitadores médicos, integraciones y referencias."
        ),
        "status": "pending", "priority": "high",
        "due_date": datetime(2026, 7, 1, 9, 0),
        "completed_at": None,
        "client": "Farmacéutica Nacional Salud Total",
        "lead": None,
        "opp_client": "Farmacéutica Nacional",
    },

    # ══ PENDING — prioridad media ════════════════════════════════════════════
    {
        "title": "Coordinar reunión de presentación con Comercializadora Rodríguez",
        "description": (
            "Agendar reunión presencial con María Isabel Rodríguez para presentar módulo "
            "de cotizaciones y facturación. Confirmar disponibilidad de sala de reuniones "
            "y preparar laptop con la demo del flujo lead → cotización → factura."
        ),
        "status": "pending", "priority": "medium",
        "due_date": datetime(2026, 6, 20, 14, 0),
        "completed_at": None,
        "client": "Comercializadora Rodríguez",
        "lead": "María Isabel Rodríguez Fallas",
        "opp_client": "Comercializadora Rodríguez",
    },
    {
        "title": "Seguimiento de cotización vencida — Desarrolladora Residencial Palmares",
        "description": (
            "Contactar a Yessenia Arce por la cotización COT-2026-039 vencida el 20 mayo. "
            "Solicitó nueva versión con énfasis en Google Ads para captación de compradores. "
            "Actualizar propuesta y reaclular valores con servicios adicionales."
        ),
        "status": "pending", "priority": "medium",
        "due_date": datetime(2026, 6, 25, 10, 0),
        "completed_at": None,
        "client": "Desarrolladora Residencial Palmares",
        "lead": None,
        "opp_client": "Desarrolladora Residencial",
    },
    {
        "title": "Validar requerimientos técnicos con Equipos Médicos Bermúdez",
        "description": (
            "Reunión técnica con José Ángel Bermúdez para revisar requerimientos de "
            "integración del CRM con sistema actual de inventario médico. Definir API "
            "de sincronización de productos y clientes. Lead activo en quote_sent."
        ),
        "status": "pending", "priority": "medium",
        "due_date": datetime(2026, 6, 25, 15, 0),
        "completed_at": None,
        "client": "Equipos Médicos Bermúdez",
        "lead": "José Ángel Bermúdez Vega",
        "opp_client": "Equipos Médicos Bermúdez",
    },
    {
        "title": "Enviar casos de éxito a Ferretería Industrial Ramírez",
        "description": (
            "Remitir a Gustavo Ramírez dos casos de éxito de empresas industriales: "
            "uno de ferretería y uno de distribuidora. Incluir métricas de retorno de "
            "inversión. Adjuntar cotización COT-2026-015 en el correo de seguimiento."
        ),
        "status": "pending", "priority": "medium",
        "due_date": datetime(2026, 6, 16, 11, 0),
        "completed_at": None,
        "client": "Ferretería Industrial Ramírez",
        "lead": "Gustavo Adolfo Ramírez Solano",
        "opp_client": "Ferretería Industrial Ramírez",
    },

    # ══ IN_PROGRESS ══════════════════════════════════════════════════════════
    {
        "title": "Negociación de contrato anual — Brenes Logística Internacional",
        "description": (
            "En proceso de revisión de términos contractuales con Arturo Brenes. "
            "Puntos pendientes: cláusula de SLA para soporte en Panamá, idioma del "
            "contrato para Colombia y condiciones de pago en cuotas trimestrales."
        ),
        "status": "in_progress", "priority": "high",
        "due_date": datetime(2026, 6, 20, 17, 0),
        "completed_at": None,
        "client": "Brenes Logística Internacional",
        "lead": "Arturo Sebastián Brenes Acosta",
        "opp_client": "Brenes Logística Internacional",
    },
    {
        "title": "Implementación fase 1 — Grupo Empresarial Alianza (Chatbot IA)",
        "description": (
            "En ejecución: configuración del chatbot de IA para WhatsApp Business de "
            "Grupo Alianza. Progreso: flujos básicos completados (70%), pendiente "
            "integración con CRM y entrenamiento con base de conocimiento del cliente."
        ),
        "status": "in_progress", "priority": "high",
        "due_date": datetime(2026, 6, 30, 17, 0),
        "completed_at": None,
        "client": "Grupo Empresarial Alianza",
        "lead": None,
        "opp_client": "Grupo Empresarial Alianza",
    },
    {
        "title": "Revisión de propuesta con Agencia Inmobiliaria Campos",
        "description": (
            "Jorge Campos solicitó ajustes en la cotización COT-2026-009: aumentar "
            "cobertura de SEO local a 12 meses y agregar módulo de fichas de propiedades. "
            "Actualizar propuesta, recalcular con nuevo ítem y enviar versión 2."
        ),
        "status": "in_progress", "priority": "medium",
        "due_date": datetime(2026, 6, 17, 12, 0),
        "completed_at": None,
        "client": "Agencia Inmobiliaria Campos",
        "lead": "Jorge Luis Campos Benavides",
        "opp_client": "Agencia Inmobiliaria Campos",
    },
    {
        "title": "Onboarding inicial — Cooperativa Agrícola del Valle Central",
        "description": (
            "Sesión de capacitación inicial para Wilberth Badilla y equipo administrativo "
            "de la Cooperativa. Temas: gestión de socios, módulo de trazabilidad y "
            "generación de reportes. Sesión grabada para referencia futura."
        ),
        "status": "in_progress", "priority": "medium",
        "due_date": datetime(2026, 6, 18, 9, 0),
        "completed_at": None,
        "client": "Cooperativa Agrícola del Valle",
        "lead": None,
        "opp_client": "Cooperativa Agrícola",
    },
    {
        "title": "Diseño de flujo de automatización — Agencia Creativa Fusión Digital",
        "description": (
            "Mapear los flujos de automatización de marketing con IA para Fusión Digital: "
            "captación de leads desde Meta Ads → calificación automática → WhatsApp → CRM. "
            "Revisar con Daniela Rojas antes del inicio del sprint de implementación."
        ),
        "status": "in_progress", "priority": "medium",
        "due_date": datetime(2026, 6, 22, 15, 0),
        "completed_at": None,
        "client": "Agencia Creativa Fusión Digital",
        "lead": None,
        "opp_client": "Agencia Creativa Fusión",
    },

    # ══ COMPLETED ════════════════════════════════════════════════════════════
    {
        "title": "Demostración del CRM a Exportaciones Café Verde S.A.",
        "description": (
            "Demo completa del módulo de trazabilidad y gestión de compradores "
            "internacionales presentada a María Fernanda Quesada. Cliente aprobó "
            "cotización COT-2026-025 al día siguiente. Proyecto activo."
        ),
        "status": "completed", "priority": "high",
        "due_date": datetime(2026, 5, 14, 10, 0),
        "completed_at": datetime(2026, 5, 14, 11, 45),
        "client": "Exportaciones Café Verde",
        "lead": None,
        "opp_client": "Exportaciones Café Verde",
    },
    {
        "title": "Reunión de cierre y firma de contrato — Importaciones JB del Caribe",
        "description": (
            "Reunión presencial con Roberto Jiménez para revisión final y firma de "
            "contrato de implementación. Documentos firmados digitalmente. "
            "Anticipo del 50% recibido. Inicio de proyecto confirmado para 1 de junio."
        ),
        "status": "completed", "priority": "high",
        "due_date": datetime(2026, 5, 27, 14, 0),
        "completed_at": datetime(2026, 5, 27, 15, 30),
        "client": "Importaciones JB del Caribe",
        "lead": "Roberto Alonso Jiménez Brenes",
        "opp_client": "Importaciones JB del Caribe",
    },
    {
        "title": "Informe mensual de SEO — Instituto Educativo Latinoamérica",
        "description": (
            "Preparación y entrega del informe mensual de posicionamiento SEO "
            "correspondiente a mayo 2026. Métricas: +34% visitas orgánicas, "
            "posición #3 en 'colegio bilingüe Heredia'. Entregado a Patricia Solís."
        ),
        "status": "completed", "priority": "medium",
        "due_date": datetime(2026, 6, 5, 12, 0),
        "completed_at": datetime(2026, 6, 5, 11, 20),
        "client": "Instituto Educativo Latinoamérica",
        "lead": None,
        "opp_client": "Instituto Educativo",
    },
    {
        "title": "Sesión de entrenamiento equipo comercial — Logística Express CA",
        "description": (
            "Capacitación de 2 horas al equipo de ventas de Logística Express: uso de "
            "módulo de oportunidades, registro de actividades y generación de cotizaciones. "
            "Asistieron 8 representantes comerciales. Evaluación aprobada por todos."
        ),
        "status": "completed", "priority": "medium",
        "due_date": datetime(2026, 5, 20, 9, 0),
        "completed_at": datetime(2026, 5, 20, 11, 0),
        "client": "Logística Express Centroamérica",
        "lead": None,
        "opp_client": "Logística Express",
    },
    {
        "title": "Revisión trimestral de resultados — Grupo Empresarial Alianza",
        "description": (
            "Reunión de revisión Q1 2026 con Ricardo Montoya. Indicadores analizados: "
            "tasa de conversión de leads (+22%), tiempo promedio de cierre (-18 días), "
            "oportunidades ganadas vs perdidas. Cliente satisfecho y renueva contrato."
        ),
        "status": "completed", "priority": "medium",
        "due_date": datetime(2026, 6, 10, 10, 0),
        "completed_at": datetime(2026, 6, 10, 11, 30),
        "client": "Grupo Empresarial Alianza",
        "lead": None,
        "opp_client": "Grupo Empresarial Alianza",
    },

    # ══ CANCELLED ════════════════════════════════════════════════════════════
    {
        "title": "Reunión de diagnóstico con Medios y Comunicaciones Caribe",
        "description": (
            "Sesión de diagnóstico para propuesta de chatbot y automatización cancelada "
            "por congelamiento de presupuesto del cliente. Diego Gamboa informó que no "
            "hay proyecciones de inversión en TI para el resto del año 2026."
        ),
        "status": "cancelled", "priority": "medium",
        "due_date": datetime(2026, 5, 5, 10, 0),
        "completed_at": None,
        "client": "Medios y Comunicaciones Caribe",
        "lead": None,
        "opp_client": "Medios y Comunicaciones",
    },
    {
        "title": "Presentación de propuesta a Distribuidora El Mercado Tropical",
        "description": (
            "Presentación de módulo e-commerce cancelada por proceso de fusión de la "
            "empresa. Ana Espinoza informó que todos los proyectos de TI están suspendidos "
            "hasta que concluya el proceso legal de fusión con el otro distribuidor."
        ),
        "status": "cancelled", "priority": "low",
        "due_date": datetime(2026, 3, 20, 14, 0),
        "completed_at": None,
        "client": "Distribuidora El Mercado Tropical",
        "lead": None,
        "opp_client": "Distribuidora El Mercado",
    },
]


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # ── Índices por nombre parcial ─────────────────────────────────────────
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct
                    WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) AS contact_id
            FROM clients c
        """)
        clients_idx = {r["name"]: {"id": r["id"], "contact_id": r["contact_id"]} for r in client_rows}

        lead_rows = await conn.fetch("SELECT id, full_name FROM leads")
        leads_idx = {r["full_name"]: r["id"] for r in lead_rows}

        opp_rows = await conn.fetch("""
            SELECT o.id, c.name as client_name
            FROM opportunities o JOIN clients c ON c.id = o.client_id
            ORDER BY CASE o.stage
                WHEN 'negotiation' THEN 1 WHEN 'quote_sent' THEN 2
                WHEN 'in_progress' THEN 3 WHEN 'meeting_scheduled' THEN 4
                ELSE 5 END
        """)
        opps_by_client: dict[str, uuid.UUID] = {}
        for r in opp_rows:
            if r["client_name"] not in opps_by_client:
                opps_by_client[r["client_name"]] = r["id"]

        def find_client(partial: str | None):
            if not partial:
                return None, None
            for name, data in clients_idx.items():
                if partial.lower() in name.lower():
                    return data["id"], data["contact_id"]
            raise ValueError(f"Cliente no encontrado: {partial!r}")

        def find_opp(partial: str | None):
            if not partial:
                return None
            for name, oid in opps_by_client.items():
                if partial.lower() in name.lower():
                    return oid
            return None

        # ── Labels para impresión ─────────────────────────────────────────────
        STATUS_ICON = {"pending": "⏳", "in_progress": "🔄", "completed": "✓ ", "cancelled": "✗ "}
        PRIORITY_COLOR = {"high": "HIGH", "medium": "MED ", "low": "LOW "}
        current_status = None

        inserted = 0
        async with conn.transaction():
            for t in TASKS:
                if t["status"] != current_status:
                    current_status = t["status"]
                    labels = {
                        "pending": "PENDIENTES", "in_progress": "EN PROGRESO",
                        "completed": "COMPLETADAS", "cancelled": "CANCELADAS",
                    }
                    print(f"\n  ── {labels[current_status]} ──")

                client_id, contact_id = find_client(t["client"])
                lead_id   = leads_idx.get(t["lead"]) if t["lead"] else None
                opp_id    = find_opp(t["opp_client"])

                await conn.execute("""
                    INSERT INTO tasks (
                        id, title, description, status, priority,
                        due_date, completed_at,
                        assigned_user_id, client_id, contact_id, lead_id, opportunity_id
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                """,
                    uuid.uuid4(),
                    t["title"], t["description"],
                    t["status"], t["priority"],
                    t["due_date"], t["completed_at"],
                    uuid.UUID(ADMIN_ID),
                    client_id, contact_id, lead_id, opp_id,
                )
                inserted += 1
                icon = STATUS_ICON[t["status"]]
                prio = PRIORITY_COLOR[t["priority"]]
                due  = t["due_date"].strftime("%d/%m/%Y") if t["due_date"] else "—"
                links = []
                if client_id:  links.append("cliente")
                if lead_id:    links.append("lead")
                if opp_id:     links.append("opp")
                print(f"  [{inserted:02d}] {icon} {prio}  {due}  [{','.join(links):18s}]  {t['title'][:52]}")

        # ── Resumen ────────────────────────────────────────────────────────────
        stats = await conn.fetch("""
            SELECT status, priority, COUNT(*) as n
            FROM tasks GROUP BY status, priority
            ORDER BY status, priority
        """)
        totals_by_status = {}
        totals_by_priority = {}
        for r in stats:
            totals_by_status[r["status"]]     = totals_by_status.get(r["status"], 0)     + r["n"]
            totals_by_priority[r["priority"]] = totals_by_priority.get(r["priority"], 0) + r["n"]

        print(f"\n{'═'*50}")
        print(f"  Por estado:")
        for s, n in totals_by_status.items():
            bar = "█" * n
            print(f"    {s:14s}  {n:>3}  {bar}")
        print(f"  Por prioridad:")
        for p, n in totals_by_priority.items():
            bar = "█" * n
            print(f"    {p:14s}  {n:>3}  {bar}")
        print(f"{'─'*50}")
        print(f"  Total insertadas: {inserted}")
        print(f"{'═'*50}")
        print(f"\n✓ {inserted} tareas insertadas correctamente.")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
