"""
Seed script: 30 actividades del CRM vinculadas a oportunidades, leads y cotizaciones.
Tipos: call(6) | email(6) | whatsapp(5) | meeting(5) | note(3)
       status_change(2) | quote_sent(2) | task_completed(1)
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_activities.py
"""
import asyncio
import uuid
from datetime import datetime
import asyncpg

DB_URL   = "postgresql://postgres:Grvn240675$$@localhost:5432/crm"
ADMIN_ID = "d06edc36-d03f-4960-864b-e71e8baee07b"

# ─── 30 actividades ───────────────────────────────────────────────────────────
# Claves de búsqueda: client_partial, lead_name, opp_client, quote_number
# Todos los campos de texto son libretos realistas del día a día de ventas.
# ─────────────────────────────────────────────────────────────────────────────
ACTIVITIES = [

    # ════════════ MEETING (5) ════════════════════════════════════════════════
    {
        "type": "meeting",
        "subject": "Reunión de diagnóstico de necesidades — Brenes Logística",
        "description": (
            "Reunión presencial de 90 minutos en las oficinas de Brenes Logística "
            "con Arturo Brenes y el Jefe de TI. Se relevaron necesidades: pipeline "
            "de ventas multipaís, cotizaciones en USD y reportes por región. "
            "Acuerdo: enviar propuesta técnica detallada en 5 días hábiles."
        ),
        "date": datetime(2026, 6, 5, 10, 0),
        "client": "Brenes Logística Internacional",
        "lead":   "Arturo Sebastián Brenes Acosta",
        "opp":    "Brenes Logística Internacional",
        "quote":  None,
    },
    {
        "type": "meeting",
        "subject": "Demo del módulo CRM inmobiliario — Agencia Campos",
        "description": (
            "Demostración de 60 minutos del CRM para el equipo de 10 asesores de la "
            "Agencia Inmobiliaria Campos. Se mostró: pipeline de propiedades, seguimiento "
            "de compradores, historial de visitas y cotizaciones. Jorge Campos solicitó "
            "añadir ficha técnica de propiedades antes de aprobar. Se revisará COT-2026-009."
        ),
        "date": datetime(2026, 7, 3, 9, 0),
        "client": "Agencia Inmobiliaria Campos",
        "lead":   "Jorge Luis Campos Benavides",
        "opp":    "Agencia Inmobiliaria Campos",
        "quote":  "COT-2026-009",
    },
    {
        "type": "meeting",
        "subject": "Reunión de revisión de propuesta — Grupo Pérez Hermanos",
        "description": (
            "Mesa de trabajo con Alejandro Pérez y gerente comercial para revisar "
            "COT-2026-022 (aprobada). Se definió cronograma de implementación en 3 fases: "
            "setup inicial (sem 1-2), capacitación (sem 3-4), go-live (sem 5). "
            "Inicio del proyecto confirmado para el 1 de junio 2026."
        ),
        "date": datetime(2026, 5, 10, 14, 0),
        "client": "Grupo Pérez Hermanos",
        "lead":   "Alejandro Pérez Gutiérrez",
        "opp":    "Grupo Pérez Hermanos",
        "quote":  "COT-2026-022",
    },
    {
        "type": "meeting",
        "subject": "Sesión de diagnóstico técnico — Tech Solutions Guzmán",
        "description": (
            "Reunión técnica de 2 horas con Diego Guzmán y el arquitecto de software de "
            "la empresa. Se mapeó el flujo actual del ERP (SAP B1) y se identificaron "
            "los endpoints de integración necesarios para la API REST del CRM. "
            "Próximo paso: envío de especificación técnica de la integración."
        ),
        "date": datetime(2026, 6, 18, 10, 30),
        "client": "Tech Solutions Guzmán",
        "lead":   "Diego Mauricio Guzmán Pérez",
        "opp":    "Tech Solutions Guzmán",
        "quote":  "COT-2026-010",
    },
    {
        "type": "meeting",
        "subject": "Reunión de cierre y firma de contrato — Importaciones JB del Caribe",
        "description": (
            "Reunión presencial de formalización con Roberto Jiménez y representante legal "
            "de Importaciones JB. Se revisó y firmó el contrato de implementación. "
            "Anticipo del 50% ($2,600) procesado vía transferencia. Kick-off agendado "
            "para el 1 de junio. Proyecto inicia con módulo de pipeline de ventas."
        ),
        "date": datetime(2026, 5, 27, 15, 0),
        "client": "Importaciones JB del Caribe",
        "lead":   "Roberto Alonso Jiménez Brenes",
        "opp":    "Importaciones JB del Caribe",
        "quote":  "COT-2026-021",
    },

    # ════════════ CALL (6) ═══════════════════════════════════════════════════
    {
        "type": "call",
        "subject": "Llamada de calificación inicial — Alejandro Pérez / Grupo Pérez Hermanos",
        "description": (
            "Llamada de 25 minutos con Alejandro Pérez. Calificación BANT: Budget definido "
            "($3,500-$4,500), Authority confirmada (es dueño), Need validada (15 vendedores "
            "usando Excel), Timeline: implementar antes de agosto 2026. Lead calificado "
            "como QUALIFIED. Siguiente paso: agendar demo personalizada."
        ),
        "date": datetime(2026, 5, 18, 9, 30),
        "client": "Grupo Pérez Hermanos",
        "lead":   "Alejandro Pérez Gutiérrez",
        "opp":    "Grupo Pérez Hermanos",
        "quote":  None,
    },
    {
        "type": "call",
        "subject": "Llamada de seguimiento de negociación — Finanzas y Crédito Mora",
        "description": (
            "Llamada de 40 minutos con Alberto Mora. Revisión de los términos de la "
            "propuesta de $9,200 para CRM financiero. Alberto solicita: reducir a $8,500 "
            "o incluir 2 meses adicionales sin costo adicional. Se acordó revisar con "
            "dirección comercial y responder en 48 horas. Alta probabilidad de cierre."
        ),
        "date": datetime(2026, 6, 8, 11, 0),
        "client": "Finanzas y Crédito Mora",
        "lead":   "Alberto Enrique Mora Badilla",
        "opp":    "Finanzas y Crédito Mora",
        "quote":  None,
    },
    {
        "type": "call",
        "subject": "Llamada de presentación y cierre — Exportaciones Café Verde",
        "description": (
            "Llamada de 30 minutos con María Fernanda Quesada. Se presentaron resultados "
            "del módulo de trazabilidad en empresa similar del sector agroexportador. "
            "Cliente confirma aprobación de COT-2026-025 ($14,916). Solicita inicio "
            "inmediato. Se agenda kick-off para siguiente semana. Oportunidad ganada."
        ),
        "date": datetime(2026, 5, 15, 14, 0),
        "client": "Exportaciones Café Verde",
        "lead":   None,
        "opp":    "Exportaciones Café Verde",
        "quote":  "COT-2026-025",
    },
    {
        "type": "call",
        "subject": "Seguimiento de cotización — Comercializadora Rodríguez e Hijos",
        "description": (
            "Llamada de 15 minutos con María Isabel Rodríguez para dar seguimiento a "
            "COT-2026-019 enviada el 25 de julio. La cliente indica que está revisando "
            "con su contador. Solicita un ejemplo del flujo de facturación electrónica. "
            "Se enviará video demostrativo por correo esta misma tarde."
        ),
        "date": datetime(2026, 7, 30, 10, 0),
        "client": "Comercializadora Rodríguez",
        "lead":   "María Isabel Rodríguez Fallas",
        "opp":    "Comercializadora Rodríguez",
        "quote":  "COT-2026-019",
    },
    {
        "type": "call",
        "subject": "Llamada de rechazo y retroalimentación — Gamboa Ingeniería Civil",
        "description": (
            "Ricardo Gamboa informó por llamada que rechazaron COT-2026-031. Razón: "
            "una firma guatemalteca ofreció implementación a $2,800 (vs $7,006). "
            "Sin soporte local ni SLA. Se documentó el caso. Cliente acepta ser "
            "recontactado en Q1 2027 si la solución externa no satisface sus necesidades."
        ),
        "date": datetime(2026, 6, 2, 16, 0),
        "client": "Gamboa Ingeniería Civil",
        "lead":   "Ricardo Antonio Gamboa Vindas",
        "opp":    "Gamboa Ingeniería Civil",
        "quote":  "COT-2026-031",
    },
    {
        "type": "call",
        "subject": "Primera llamada de contacto — Gustavo Ramírez / Ferretería Industrial",
        "description": (
            "Llamada entrante de Gustavo Ramírez, referido por Constructora Los Pinos. "
            "Comentó necesidad de digitalizar cotizaciones para clientes constructores. "
            "Cartera actual: 45 clientes corporativos. Interés en módulo de crédito por "
            "cliente. Se agendó reunión presencial en Alajuela para el 20 de junio."
        ),
        "date": datetime(2026, 6, 10, 9, 0),
        "client": "Ferretería Industrial Ramírez",
        "lead":   "Gustavo Adolfo Ramírez Solano",
        "opp":    "Ferretería Industrial Ramírez",
        "quote":  None,
    },

    # ════════════ EMAIL (6) ══════════════════════════════════════════════════
    {
        "type": "email",
        "subject": "Envío de brochure y casos de éxito — Diego Guzmán / Tech Solutions",
        "description": (
            "Correo enviado a dguzman@techsolutions.cr con adjuntos: brochure corporativo "
            "del CRM, caso de éxito de empresa TI con integración ERP, y especificación "
            "técnica de la API REST. Asunto: 'Material solicitado — CRM + SAP B1'. "
            "Confirmación de lectura recibida a las 2 horas."
        ),
        "date": datetime(2026, 5, 26, 11, 0),
        "client": "Tech Solutions Guzmán",
        "lead":   "Diego Mauricio Guzmán Pérez",
        "opp":    "Tech Solutions Guzmán",
        "quote":  None,
    },
    {
        "type": "email",
        "subject": "Confirmación de demo agendada — Manuel Quesada / Agrícola Los Naranjos",
        "description": (
            "Correo de confirmación enviado a mquesada@losnaranjos.cr con agenda de la "
            "demo: 10am del 15 jun, vía Google Meet. Enlace adjunto. Se incluye temario: "
            "1) Gestión de compradores int'l, 2) Control de contratos, 3) Trazabilidad. "
            "Solicitar al cliente traer datos de sus 3 principales compradores."
        ),
        "date": datetime(2026, 6, 6, 8, 30),
        "client": "Agrícola Los Naranjos",
        "lead":   "Manuel Antonio Quesada Ulate",
        "opp":    "Agrícola Los Naranjos",
        "quote":  "COT-2026-011",
    },
    {
        "type": "email",
        "subject": "Aprobación de cotización confirmada — Grupo Empresarial Alianza",
        "description": (
            "Correo recibido de Ricardo Montoya confirmando aprobación de COT-2026-026 "
            "($6,915.60 con descuento del 15%). Adjuntó orden de compra interna #OC-2026-0088. "
            "Se generó factura proforma y se coordinó inicio de implementación del "
            "chatbot de IA para el 5 de mayo. Cliente muy comprometido con el proyecto."
        ),
        "date": datetime(2026, 4, 28, 15, 30),
        "client": "Grupo Empresarial Alianza",
        "lead":   None,
        "opp":    "Grupo Empresarial Alianza",
        "quote":  "COT-2026-026",
    },
    {
        "type": "email",
        "subject": "Respuesta a consultas técnicas de COT-2026-014 — Brenes Logística",
        "description": (
            "Arturo Brenes envió 5 consultas técnicas sobre la propuesta de CRM multipaís. "
            "Se respondió detalladamente: disponibilidad de app móvil (sí, iOS y Android), "
            "soporte en español y portugués (sí), backup diario automático (sí), "
            "SLA de soporte < 4 horas (con plan Premium). Respuesta enviada en 2 horas."
        ),
        "date": datetime(2026, 7, 12, 14, 0),
        "client": "Brenes Logística Internacional",
        "lead":   "Arturo Sebastián Brenes Acosta",
        "opp":    "Brenes Logística Internacional",
        "quote":  "COT-2026-014",
    },
    {
        "type": "email",
        "subject": "Notificación de vencimiento — COT-2026-037 Hotel Brisas del Atlántico",
        "description": (
            "Correo enviado a h.mena@lasbrisasatlantico.com notificando el vencimiento de "
            "COT-2026-037 el 31 de mayo. Se adjunta nueva versión actualizada con precios "
            "vigentes y se propone reunión virtual para revisar el alcance antes de la "
            "temporada alta diciembre 2026 - abril 2027. Se solicita respuesta a la brevedad."
        ),
        "date": datetime(2026, 6, 5, 9, 0),
        "client": "Hotel & Spa Las Brisas",
        "lead":   None,
        "opp":    "Hotel & Spa Las Brisas",
        "quote":  "COT-2026-037",
    },
    {
        "type": "email",
        "subject": "Ajustes solicitados en propuesta — Centro Educativo Bilingüe Prado",
        "description": (
            "Mariela Prado solicitó por correo dos modificaciones a COT-2026-017: "
            "1) Incluir módulo de notificaciones a padres de familia (SMS/WhatsApp), "
            "2) Ampliar plan de Redes Sociales a 12 meses. Se indicó que se prepara "
            "versión 2 con los ajustes y recalculo de precio en 48 horas hábiles."
        ),
        "date": datetime(2026, 7, 23, 10, 0),
        "client": "Centro Educativo Bilingüe Prado",
        "lead":   "Mariela Gabriela Prado Arce",
        "opp":    "Centro Educativo Bilingüe Prado",
        "quote":  "COT-2026-017",
    },

    # ════════════ WHATSAPP (5) ═══════════════════════════════════════════════
    {
        "type": "whatsapp",
        "subject": "Contacto inicial por WhatsApp — Arturo Brenes / Brenes Logística",
        "description": (
            "Mensaje recibido de +506 8867-4422 (Arturo Brenes): 'Buenos días, me llegó "
            "una campaña de correo sobre su CRM. Manejamos rutas en 3 países, ¿tienen "
            "algo para empresas de logística?' Se respondió en 15 min con presentación "
            "de 1 página y enlace para agendar demo. Lead calificado ese mismo día."
        ),
        "date": datetime(2026, 5, 16, 8, 45),
        "client": "Brenes Logística Internacional",
        "lead":   "Arturo Sebastián Brenes Acosta",
        "opp":    "Brenes Logística Internacional",
        "quote":  None,
    },
    {
        "type": "whatsapp",
        "subject": "Confirmación de reunión — María Isabel Rodríguez / Comercializadora",
        "description": (
            "Intercambio de mensajes con María Isabel Rodríguez (8891-7788) para confirmar "
            "la reunión del 20 de junio. Envió ubicación de sus oficinas en Desamparados. "
            "Se confirmó presencia del contador y de una vendedora para la demo del módulo "
            "de cotizaciones. Se recordó traer laptop o tablet para práctica en vivo."
        ),
        "date": datetime(2026, 6, 9, 14, 30),
        "client": "Comercializadora Rodríguez",
        "lead":   "María Isabel Rodríguez Fallas",
        "opp":    "Comercializadora Rodríguez",
        "quote":  None,
    },
    {
        "type": "whatsapp",
        "subject": "Envío de casos de éxito — Gustavo Ramírez / Ferretería Industrial",
        "description": (
            "Se enviaron por WhatsApp a +506 8834-5500: PDF con caso de éxito de "
            "distribuidora industrial similar (aumento del 28% en cierre de ventas), "
            "video de 3 min del módulo de cotizaciones y enlace de la cotización "
            "COT-2026-015. Gustavo respondió: 'Lo veo esta tarde, gracias.' "
        ),
        "date": datetime(2026, 7, 1, 11, 30),
        "client": "Ferretería Industrial Ramírez",
        "lead":   "Gustavo Adolfo Ramírez Solano",
        "opp":    "Ferretería Industrial Ramírez",
        "quote":  "COT-2026-015",
    },
    {
        "type": "whatsapp",
        "subject": "Seguimiento post-reunión — Ana Patricia Salas / Asesoría Contable",
        "description": (
            "Mensaje enviado a Ana Salas (+506 8901-1122) luego de la primera reunión: "
            "'Hola Ana, un gusto reunirme con usted hoy. Le adjunto el resumen de lo "
            "conversado y la cotización COT-2026-034. Quedo atento a sus consultas.' "
            "Ana respondió: 'Gracias, lo reviso con calma esta semana.'"
        ),
        "date": datetime(2026, 5, 12, 16, 0),
        "client": "Asesoría Contable Salas",
        "lead":   "Ana Patricia Salas Ureña",
        "opp":    "Asesoría Contable Salas",
        "quote":  None,
    },
    {
        "type": "whatsapp",
        "subject": "Alerta de vencimiento de cotización — Soluciones Financieras del Sur",
        "description": (
            "Mensaje enviado a Andrés Ospina (+57 310 456-7890) recordando que la "
            "cotización COT-2026-036 vence el 30 de abril: 'Andrés, buen día. Les "
            "recuerdo que la propuesta de CRM vence este lunes. ¿Hay algún bloqueo '  "
            "que pueda ayudarle a resolver?' Andrés respondió que el contacto salió "
            "de la empresa y el proyecto quedó en pausa."
        ),
        "date": datetime(2026, 4, 28, 9, 0),
        "client": "Soluciones Financieras del Sur",
        "lead":   None,
        "opp":    "Soluciones Financieras del Sur",
        "quote":  "COT-2026-036",
    },

    # ════════════ NOTE (3) ═══════════════════════════════════════════════════
    {
        "type": "note",
        "subject": "Notas de diagnóstico — Ferretería Industrial Ramírez",
        "description": (
            "Notas internas post-reunión de diagnóstico con Gustavo Ramírez:\n"
            "- Cartera: 45 clientes corporativos (constructoras y contratistas)\n"
            "- Proceso actual: cotizaciones en Excel, envío por correo, sin seguimiento\n"
            "- Problemas: duplicidad de cotizaciones, pérdida de seguimiento, sin historial\n"
            "- Prioridad: módulo de cotizaciones con crédito por cliente\n"
            "- Decisor único: Gustavo. Timeline: 2 meses. Budget: ~$3,000-$3,500."
        ),
        "date": datetime(2026, 6, 3, 17, 0),
        "client": "Ferretería Industrial Ramírez",
        "lead":   "Gustavo Adolfo Ramírez Solano",
        "opp":    "Ferretería Industrial Ramírez",
        "quote":  None,
    },
    {
        "type": "note",
        "subject": "Perfil de calificación — José Ángel Bermúdez / Equipos Médicos",
        "description": (
            "Notas de calificación del lead José Ángel Bermúdez:\n"
            "- Empresa: distribuidora de equipos médicos a clínicas y hospitales\n"
            "- Equipo comercial: 6 visitadores médicos en campo\n"
            "- Sistema actual: ninguno (gestión por WhatsApp y agenda personal)\n"
            "- Necesidad crítica: catálogo técnico digital y cotizaciones profesionales\n"
            "- Budget: confirmado ~$5,000-$6,500 anuales\n"
            "- Riesgo: proceso de compra largo por aprobación de socios."
        ),
        "date": datetime(2026, 6, 4, 15, 0),
        "client": "Equipos Médicos Bermúdez",
        "lead":   "José Ángel Bermúdez Vega",
        "opp":    "Equipos Médicos Bermúdez",
        "quote":  None,
    },
    {
        "type": "note",
        "subject": "Observaciones post-onboarding — Cooperativa Agrícola del Valle Central",
        "description": (
            "Notas de la sesión de onboarding con Wilberth Badilla y 4 colaboradores:\n"
            "- Nivel técnico del equipo: básico. Requieren manual simplificado en PDF.\n"
            "- Proceso más valorado: registro de producción entregada por asociado.\n"
            "- Pendiente: configurar campos personalizados para tipo de cultivo y zona.\n"
            "- Solicitud adicional: capacitación extra para el tesorero (2 horas más).\n"
            "- NPS preliminar: 8/10. Cliente satisfecho con la funcionalidad básica."
        ),
        "date": datetime(2026, 6, 20, 18, 0),
        "client": "Cooperativa Agrícola del Valle",
        "lead":   None,
        "opp":    "Cooperativa Agrícola",
        "quote":  None,
    },

    # ════════════ STATUS_CHANGE (2) ══════════════════════════════════════════
    {
        "type": "status_change",
        "subject": "Oportunidad avanzó a Negociación — Seguridad Privada Fortis S.A.",
        "description": (
            "La oportunidad 'Gestión de contratos corporativos — Seguridad Fortis' avanzó "
            "de etapa 'quote_sent' a 'negotiation'. Motivo: Ernesto Picado confirmó "
            "interés en cerrar antes del 31 de julio. Se inician negociaciones sobre "
            "términos de SLA de soporte y condiciones de pago en cuotas trimestrales."
        ),
        "date": datetime(2026, 6, 1, 10, 0),
        "client": "Seguridad Privada Fortis",
        "lead":   "Ernesto Guillermo Picado Mora",
        "opp":    "Seguridad Privada Fortis",
        "quote":  None,
    },
    {
        "type": "status_change",
        "subject": "Oportunidad marcada como GANADA — Logística Express Centroamérica",
        "description": (
            "La oportunidad 'Implementación inicial CRM — Logística Express CA' fue "
            "marcada como WON. Contrato firmado por Ernesto Aguilar el 15 de marzo 2026. "
            "Valor cerrado: $6,800 USD. Anticipo 50% recibido ($3,400). Proyecto de "
            "implementación iniciado. Equipo de 8 vendedores incorporados al sistema."
        ),
        "date": datetime(2026, 3, 15, 16, 0),
        "client": "Logística Express Centroamérica",
        "lead":   None,
        "opp":    "Logística Express Centroamérica",
        "quote":  "COT-2026-023",
    },

    # ════════════ QUOTE_SENT (2) ═════════════════════════════════════════════
    {
        "type": "quote_sent",
        "subject": "Cotización COT-2026-011 enviada — Agrícola Los Naranjos S.A.",
        "description": (
            "Cotización COT-2026-011 enviada por correo y WhatsApp a Manuel Quesada "
            "(mquesada@losnaranjos.cr / +506 8778-3300). Monto: $15,424.50 USD con IVA. "
            "Incluye: SEO Internacional (6 meses), Plan Marketing 360°, Google Ads (3 "
            "meses) y Redes Sociales Pro (3 meses). Vigencia: 30 días. Se hizo seguimiento "
            "telefónico al día siguiente para confirmar recepción."
        ),
        "date": datetime(2026, 7, 5, 9, 30),
        "client": "Agrícola Los Naranjos",
        "lead":   "Manuel Antonio Quesada Ulate",
        "opp":    "Agrícola Los Naranjos",
        "quote":  "COT-2026-011",
    },
    {
        "type": "quote_sent",
        "subject": "Cotización COT-2026-018 enviada — Consultoría RH Blanco & Partners",
        "description": (
            "Cotización COT-2026-018 ($6,441.00 con IVA) enviada a rblanco@rhblancopartners.com. "
            "Incluye: 2 Landing Pages de conversión, Google Ads (4 meses), Meta Ads (4 meses) "
            "y configuración inicial de campañas. Se adjuntó caso de éxito de otra firma de "
            "RRHH que incrementó leads calificados en un 40% en 90 días."
        ),
        "date": datetime(2026, 7, 15, 11, 0),
        "client": "Consultoría RH Blanco",
        "lead":   "Rebeca Tatiana Blanco Vásquez",
        "opp":    "Consultoría RH Blanco",
        "quote":  "COT-2026-018",
    },

    # ════════════ TASK_COMPLETED (1) ═════════════════════════════════════════
    {
        "type": "task_completed",
        "subject": "Capacitación completada — Equipo comercial Logística Express CA",
        "description": (
            "Tarea de capacitación completada exitosamente. Se entrenó a 8 representantes "
            "comerciales de Logística Express en: módulo de oportunidades, registro de "
            "actividades (llamadas, emails, WhatsApp) y generación de cotizaciones PDF. "
            "Tiempo de sesión: 2 horas. Evaluación de conocimiento: promedio 8.6/10. "
            "Material de soporte enviado a todos los participantes por correo."
        ),
        "date": datetime(2026, 5, 20, 11, 0),
        "client": "Logística Express Centroamérica",
        "lead":   None,
        "opp":    "Logística Express Centroamérica",
        "quote":  None,
    },
]

TYPE_ICONS = {
    "call": "📞", "email": "✉️ ", "whatsapp": "💬", "meeting": "🤝",
    "note": "📝", "status_change": "🔀", "quote_sent": "📄", "task_completed": "✅",
}


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # ── Índices ────────────────────────────────────────────────────────────
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct
                    WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) AS contact_id
            FROM clients c
        """)
        clients_idx = {r["name"]: {"id": r["id"], "contact_id": r["contact_id"]}
                       for r in client_rows}

        lead_rows = await conn.fetch("SELECT id, full_name FROM leads")
        leads_idx = {r["full_name"]: r["id"] for r in lead_rows}

        opp_rows = await conn.fetch("""
            SELECT o.id, c.name AS client_name
            FROM opportunities o JOIN clients c ON c.id = o.client_id
            ORDER BY CASE o.stage
                WHEN 'won' THEN 1 WHEN 'negotiation' THEN 2
                WHEN 'quote_sent' THEN 3 ELSE 4 END
        """)
        opps_by_client: dict[str, uuid.UUID] = {}
        for r in opp_rows:
            if r["client_name"] not in opps_by_client:
                opps_by_client[r["client_name"]] = r["id"]

        quote_rows = await conn.fetch(
            "SELECT id, quote_number, client_id FROM quotes"
        )
        quotes_idx = {r["quote_number"]: r["id"] for r in quote_rows}

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

        # ── Inserción ─────────────────────────────────────────────────────────
        inserted      = 0
        current_type  = None
        type_labels = {
            "meeting": "REUNIÓN", "call": "LLAMADA", "email": "EMAIL",
            "whatsapp": "WHATSAPP", "note": "NOTA",
            "status_change": "CAMBIO DE ESTADO", "quote_sent": "COTIZACIÓN ENVIADA",
            "task_completed": "TAREA COMPLETADA",
        }

        async with conn.transaction():
            for act in ACTIVITIES:
                if act["type"] != current_type:
                    current_type = act["type"]
                    icon = TYPE_ICONS[current_type]
                    print(f"\n  ── {icon} {type_labels[current_type]} ──")

                client_id, contact_id = find_client(act["client"])
                lead_id  = leads_idx.get(act["lead"]) if act["lead"] else None
                opp_id   = find_opp(act["opp"])
                quote_id = quotes_idx.get(act["quote"]) if act["quote"] else None

                await conn.execute("""
                    INSERT INTO activities (
                        id, activity_type, subject, description,
                        user_id, client_id, contact_id,
                        lead_id, opportunity_id, quote_id, activity_date
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
                """,
                    uuid.uuid4(),
                    act["type"], act["subject"], act["description"],
                    uuid.UUID(ADMIN_ID),
                    client_id, contact_id,
                    lead_id, opp_id, quote_id,
                    act["date"],
                )
                inserted += 1

                links = []
                if client_id: links.append("cli")
                if lead_id:   links.append("lead")
                if opp_id:    links.append("opp")
                if quote_id:  links.append("quote")

                fecha = act["date"].strftime("%d/%m/%Y")
                print(f"  [{inserted:02d}] {fecha}  [{','.join(links):16s}]  {act['subject'][:55]}")

        # ── Resumen ────────────────────────────────────────────────────────────
        stats = await conn.fetch("""
            SELECT activity_type, COUNT(*) as n
            FROM activities GROUP BY activity_type ORDER BY n DESC
        """)
        total = await conn.fetchval("SELECT COUNT(*) FROM activities")

        print(f"\n{'═'*55}")
        print(f"  {'TIPO':20s} {'#':>4}  {'BARRA':30s}")
        print(f"  {'─'*52}")
        for r in stats:
            icon = TYPE_ICONS.get(r["activity_type"], "  ")
            bar  = "█" * int(r["n"])
            print(f"  {icon} {r['activity_type']:18s} {r['n']:>4}  {bar}")
        print(f"  {'─'*52}")
        print(f"  {'TOTAL':20s} {total:>4}")
        print(f"{'═'*55}")
        print(f"\n✓ {inserted} actividades insertadas correctamente.")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
