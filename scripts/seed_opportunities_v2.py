"""
Seed script v2: 30 oportunidades correctamente enlazadas.
  - 70% (21): cliente creado desde el lead → lead_id + client_id coherentes
  - 30%  (9): cliente existente sin lead → solo client_id
Borra las oportunidades previas antes de insertar.
Ejecutar desde la raíz del proyecto con el venv activo:
    python scripts/seed_opportunities_v2.py
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

# ─────────────────────────────────────────────────────────────────────────────
# 70% — 21 oportunidades desde leads
# Cada item: lead_full_name, datos del nuevo cliente, datos del contacto (=el lead),
#             datos de la oportunidad.
# ─────────────────────────────────────────────────────────────────────────────
LEAD_OPPS = [
    # ── GANADAS ──────────────────────────────────────────────────────────────
    {
        "lead": "Roberto Alonso Jiménez Brenes",
        "client": {
            "name": "Importaciones JB del Caribe S.A.",
            "industry": "Importación y Exportación",
            "phone": "+506 2270-5566", "email": "info@jbcaribe.com",
            "website": "https://www.jbcaribe.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Zona Industrial Pavas, Bodega 14-B",
            "status": "active", "tax_id": "3-101-812345",
        },
        "contact": {
            "full_name": "Roberto Alonso Jiménez Brenes",
            "position": "Gerente General",
            "email": "rjimenez@jbcaribe.com",
            "phone": "+506 2270-5566", "whatsapp": "+506 8856-5566",
        },
        "opp": {
            "title": "CRM multipaís para equipo comercial — JB del Caribe",
            "description": "Implementación de CRM para empresa importadora con operaciones en CR, PAN y COL. Pipeline de ventas para equipo de 15 representantes, módulo de cotizaciones multimoneda y reportes consolidados.",
            "stage": "won", "value": 5200.00,
            "close": date(2026, 5, 30), "closed_at": datetime(2026, 5, 30, 14, 0),
            "lost_reason": None,
        },
    },
    {
        "lead": "Alejandro Pérez Gutiérrez",
        "client": {
            "name": "Grupo Pérez Hermanos S.A.",
            "industry": "Distribución y Comercio",
            "phone": "+506 2290-4411", "email": "contacto@gpherms.com",
            "website": "https://www.gpherms.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Uruca, Ave. 10, Edificio Los Cedros, Piso 2",
            "status": "active", "tax_id": "3-101-823456",
        },
        "contact": {
            "full_name": "Alejandro Pérez Gutiérrez",
            "position": "Director Comercial",
            "email": "alejandro.perez@gpherms.com",
            "phone": "+506 2290-4411", "whatsapp": "+506 8810-4411",
        },
        "opp": {
            "title": "CRM para equipo de ventas — Grupo Pérez Hermanos",
            "description": "CRM completo para automatizar seguimiento de ventas de 15 representantes comerciales. Módulos de leads, oportunidades, cotizaciones y dashboards ejecutivos.",
            "stage": "won", "value": 3800.00,
            "close": date(2026, 5, 20), "closed_at": datetime(2026, 5, 20, 10, 0),
            "lost_reason": None,
        },
    },
    # ── PERDIDA ───────────────────────────────────────────────────────────────
    {
        "lead": "Ricardo Antonio Gamboa Vindas",
        "client": {
            "name": "Gamboa Ingeniería Civil S.A.",
            "industry": "Arquitectura e Ingeniería",
            "phone": "+506 2441-0055", "email": "info@gamboaing.cr",
            "website": "https://www.gamboaing.cr",
            "country": "Costa Rica", "city": "Alajuela",
            "address": "La Garita, frente a Panasonic, Edificio Gamma",
            "status": "inactive", "tax_id": "3-101-756234",
        },
        "contact": {
            "full_name": "Ricardo Antonio Gamboa Vindas",
            "position": "Socio Fundador",
            "email": "rgamboa@gamboaing.cr",
            "phone": "+506 2441-0055", "whatsapp": "+506 8823-0055",
        },
        "opp": {
            "title": "Pipeline de licitaciones para Gamboa Ingeniería Civil",
            "description": "CRM para gestión de licitaciones públicas y privadas, seguimiento de propuestas técnicas, control de etapas y gestión de subcontratistas.",
            "stage": "lost", "value": 5500.00,
            "close": date(2026, 6, 1), "closed_at": datetime(2026, 6, 1, 9, 0),
            "lost_reason": "El cliente contrató con una firma extranjera que ofreció precio significativamente menor. No fue posible competir en costo en esta oportunidad.",
        },
    },
    # ── NEGOCIACIÓN ───────────────────────────────────────────────────────────
    {
        "lead": "Arturo Sebastián Brenes Acosta",
        "client": {
            "name": "Brenes Logística Internacional",
            "industry": "Distribución y Logística",
            "phone": "+506 2277-4422", "email": "operaciones@breneslogi.com",
            "website": "https://www.breneslogi.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Zona Franca Metropolitana, Módulo 8, Bodega C",
            "status": "prospect", "tax_id": "3-102-634521",
        },
        "contact": {
            "full_name": "Arturo Sebastián Brenes Acosta",
            "position": "Gerente Regional de Ventas",
            "email": "abrenes@breneslogi.com",
            "phone": "+506 2277-4422", "whatsapp": "+506 8867-4422",
        },
        "opp": {
            "title": "CRM regional multipaís — Brenes Logística CR-PAN-COL",
            "description": "CRM unificado para empresa logística con operaciones en Costa Rica, Panamá y Colombia. Gestión de clientes corporativos, cotizaciones de rutas y reportes de rentabilidad por país.",
            "stage": "negotiation", "value": 7800.00,
            "close": date(2026, 7, 31), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Alberto Enrique Mora Badilla",
        "client": {
            "name": "Finanzas y Crédito Mora S.A.",
            "industry": "Finanzas",
            "phone": "+506 2290-3322", "email": "info@financredito.com",
            "website": "https://www.financredito.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Barrio Tournón, Calle 21, Edificio Finance Center, Piso 5",
            "status": "prospect", "tax_id": "3-101-945678",
        },
        "contact": {
            "full_name": "Alberto Enrique Mora Badilla",
            "position": "Director Ejecutivo",
            "email": "amora@financredito.com",
            "phone": "+506 2290-3322", "whatsapp": "+506 8801-3322",
        },
        "opp": {
            "title": "CRM financiero para cartera de 800 clientes activos",
            "description": "Plataforma CRM para financiera: seguimiento de prospectos, gestión y segmentación de cartera, alertas de vencimiento, embudo de captación y reportes de retención.",
            "stage": "negotiation", "value": 9200.00,
            "close": date(2026, 8, 15), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Ernesto Guillermo Picado Mora",
        "client": {
            "name": "Seguridad Privada Fortis S.A.",
            "industry": "Seguridad Privada",
            "phone": "+506 2256-7788", "email": "contratos@seguridadfortis.cr",
            "website": "https://www.seguridadfortis.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "La Uruca, detrás del Museo del Niño, Bodega 3",
            "status": "prospect", "tax_id": "3-101-689012",
        },
        "contact": {
            "full_name": "Ernesto Guillermo Picado Mora",
            "position": "Gerente de Operaciones",
            "email": "epicado@seguridadfortis.cr",
            "phone": "+506 2256-7788", "whatsapp": "+506 8845-7788",
        },
        "opp": {
            "title": "Gestión de contratos corporativos — Seguridad Fortis",
            "description": "CRM para gestión de contratos de seguridad privada: clientes corporativos, renovaciones automáticas, control de servicios prestados, SLAs y facturación mensual recurrente.",
            "stage": "negotiation", "value": 4500.00,
            "close": date(2026, 7, 31), "closed_at": None, "lost_reason": None,
        },
    },
    # ── COTIZACIÓN ENVIADA ────────────────────────────────────────────────────
    {
        "lead": "Jorge Luis Campos Benavides",
        "client": {
            "name": "Agencia Inmobiliaria Campos",
            "industry": "Bienes Raíces",
            "phone": "+506 2222-6677", "email": "info@inmobcampos.cr",
            "website": "https://www.inmobcampos.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "Santa Ana, Centro Comercial Lindora, Local 8",
            "status": "prospect", "tax_id": "3-102-512890",
        },
        "contact": {
            "full_name": "Jorge Luis Campos Benavides",
            "position": "Propietario y Corredor Principal",
            "email": "jcampos@inmobcampos.cr",
            "phone": "+506 2222-6677", "whatsapp": "+506 8812-6677",
        },
        "opp": {
            "title": "CRM inmobiliario con pipeline de propiedades — Campos",
            "description": "CRM para agencia inmobiliaria con 10 asesores. Pipeline de propiedades, seguimiento de compradores y arrendatarios, historial de visitas y generación de cotizaciones.",
            "stage": "quote_sent", "value": 4200.00,
            "close": date(2026, 7, 20), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Diego Mauricio Guzmán Pérez",
        "client": {
            "name": "Tech Solutions Guzmán S.A.",
            "industry": "Tecnología",
            "phone": "+506 2290-7788", "email": "hola@techsolutions.cr",
            "website": "https://www.techsolutions.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "Escazú, Multiplaza, Torre Empresarial, Oficina 402",
            "status": "prospect", "tax_id": "3-102-478901",
        },
        "contact": {
            "full_name": "Diego Mauricio Guzmán Pérez",
            "position": "CEO y Fundador",
            "email": "dguzman@techsolutions.cr",
            "phone": "+506 2290-7788", "whatsapp": "+506 8845-7788",
        },
        "opp": {
            "title": "Integración CRM + ERP vía API — Tech Solutions Guzmán",
            "description": "Proyecto de integración del CRM con ERP existente mediante API REST. Sincronización de clientes, oportunidades y facturas. Pipeline de ventas para empresa de TI.",
            "stage": "quote_sent", "value": 6500.00,
            "close": date(2026, 7, 25), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Manuel Antonio Quesada Ulate",
        "client": {
            "name": "Agrícola Los Naranjos S.A.",
            "industry": "Agro-exportación",
            "phone": "+506 2462-3300", "email": "exporta@losnaranjos.cr",
            "website": "https://www.losnaranjos.cr",
            "country": "Costa Rica", "city": "Alajuela",
            "address": "Orotina, Finca Los Naranjos, Km 8 carretera a Puntarenas",
            "status": "prospect", "tax_id": "3-101-345678",
        },
        "contact": {
            "full_name": "Manuel Antonio Quesada Ulate",
            "position": "Gerente de Exportaciones",
            "email": "mquesada@losnaranjos.cr",
            "phone": "+506 2462-3300", "whatsapp": "+506 8778-3300",
        },
        "opp": {
            "title": "CRM de compradores internacionales — Agrícola Los Naranjos",
            "description": "CRM para exportadora de piña: gestión de compradores internacionales, historial de exportaciones por cliente, contratos, cumplimiento de pedidos y trazabilidad.",
            "stage": "quote_sent", "value": 4800.00,
            "close": date(2026, 8, 5), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Lorena Beatriz Arias Méndez",
        "client": {
            "name": "Arias & Méndez Arquitectos",
            "industry": "Arquitectura e Ingeniería",
            "phone": "+506 2290-0011", "email": "info@ariasmendezcr.com",
            "website": "https://www.ariasmendezcr.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Curridabat, Avenida Los Yoses, Casa 55",
            "status": "prospect", "tax_id": "3-102-389012",
        },
        "contact": {
            "full_name": "Lorena Beatriz Arias Méndez",
            "position": "Socia Directora",
            "email": "larias@ariasmendezcr.com",
            "phone": "+506 2290-0011", "whatsapp": "+506 8823-0011",
        },
        "opp": {
            "title": "Gestión de proyectos y cotizaciones — Arias & Méndez Arq.",
            "description": "CRM para firma de arquitectura: control de proyectos en cada etapa, cotizaciones por fase de obra, historial de reuniones con clientes y reportes de rentabilidad por proyecto.",
            "stage": "quote_sent", "value": 3100.00,
            "close": date(2026, 8, 10), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "José Ángel Bermúdez Vega",
        "client": {
            "name": "Equipos Médicos Bermúdez S.A.",
            "industry": "Salud",
            "phone": "+506 2234-7711", "email": "ventas@equimedber.com",
            "website": "https://www.equimedber.com",
            "country": "Costa Rica", "city": "San José",
            "address": "San Pedro, frente al Hospital Clínica Bíblica, Edificio Médico 3",
            "status": "prospect", "tax_id": "3-101-923456",
        },
        "contact": {
            "full_name": "José Ángel Bermúdez Vega",
            "position": "Gerente de Ventas",
            "email": "jbermudez@equimedber.com",
            "phone": "+506 2234-7711", "whatsapp": "+506 8856-7711",
        },
        "opp": {
            "title": "CRM de ventas para distribuidora de equipos médicos",
            "description": "Pipeline de ventas B2B para equipos médicos: seguimiento de prospectos clínicas y hospitales, historial de demostraciones, cotizaciones técnicas y contratos de mantenimiento.",
            "stage": "quote_sent", "value": 5800.00,
            "close": date(2026, 7, 30), "closed_at": None, "lost_reason": None,
        },
    },
    # ── DIAGNÓSTICO HECHO ─────────────────────────────────────────────────────
    {
        "lead": "Ana Patricia Salas Ureña",
        "client": {
            "name": "Asesoría Contable Salas",
            "industry": "Servicios Financieros",
            "phone": "+506 2280-1122", "email": "info@asesoriasalas.cr",
            "website": "https://www.asesoriasalas.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "Rohrmoser, Residencial Los Pinos, Casa 14",
            "status": "prospect", "tax_id": "3-101-234567",
        },
        "contact": {
            "full_name": "Ana Patricia Salas Ureña",
            "position": "Propietaria y Contadora",
            "email": "asalas@asesoriasalas.cr",
            "phone": "+506 2280-1122", "whatsapp": "+506 8901-1122",
        },
        "opp": {
            "title": "Seguimiento de clientes y tareas — Asesoría Contable Salas",
            "description": "Módulo de CRM para firma contable: control de clientes, tareas con recordatorios por vencimientos fiscales, historial de reuniones y documentos por cliente.",
            "stage": "diagnosis_done", "value": 1800.00,
            "close": date(2026, 9, 5), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Gustavo Adolfo Ramírez Solano",
        "client": {
            "name": "Ferretería Industrial Ramírez S.A.",
            "industry": "Comercio Industrial",
            "phone": "+506 2460-5500", "email": "ventas@ferreind.cr",
            "website": "https://www.ferreind.cr",
            "country": "Costa Rica", "city": "Alajuela",
            "address": "Ciudad Quesada, Barrio Industrial, 300 m norte del ICE",
            "status": "prospect", "tax_id": "3-101-467890",
        },
        "contact": {
            "full_name": "Gustavo Adolfo Ramírez Solano",
            "position": "Gerente de Ventas",
            "email": "gramírez@ferreind.cr",
            "phone": "+506 2460-5500", "whatsapp": "+506 8834-5500",
        },
        "opp": {
            "title": "Cotizaciones y clientes corporativos — Ferretería Ramírez",
            "description": "Módulo de gestión de clientes constructoras para ferretería industrial. Catálogo de productos, cotizaciones digitales, control de crédito por cliente y seguimiento de pedidos.",
            "stage": "diagnosis_done", "value": 2800.00,
            "close": date(2026, 9, 15), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Mariela Gabriela Prado Arce",
        "client": {
            "name": "Centro Educativo Bilingüe Prado",
            "industry": "Educación",
            "phone": "+506 2250-0044", "email": "admisiones@cebprado.edu.cr",
            "website": "https://www.cebprado.edu.cr",
            "country": "Costa Rica", "city": "Heredia",
            "address": "Heredia Centro, 200 m norte del Banco Nacional",
            "status": "prospect", "tax_id": "3-008-345678",
        },
        "contact": {
            "full_name": "Mariela Gabriela Prado Arce",
            "position": "Directora Académica",
            "email": "mprado@cebprado.edu.cr",
            "phone": "+506 2250-0044", "whatsapp": "+506 8823-0044",
        },
        "opp": {
            "title": "Módulo de admisiones y seguimiento — Colegio Bilingüe Prado",
            "description": "CRM educativo: seguimiento del proceso de admisiones desde primer contacto de familias hasta matrícula. Automatización de comunicaciones, documentos requeridos y estadísticas por cohorte.",
            "stage": "diagnosis_done", "value": 4100.00,
            "close": date(2026, 9, 20), "closed_at": None, "lost_reason": None,
        },
    },
    # ── REUNIÓN AGENDADA ──────────────────────────────────────────────────────
    {
        "lead": "María Isabel Rodríguez Fallas",
        "client": {
            "name": "Comercializadora Rodríguez e Hijos",
            "industry": "Distribución y Logística",
            "phone": "+506 2234-7788", "email": "info@comercializadorarf.com",
            "website": "https://www.comercializadorarf.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Desamparados, Calle Fátima, Local 3",
            "status": "prospect", "tax_id": "3-101-734521",
        },
        "contact": {
            "full_name": "María Isabel Rodríguez Fallas",
            "position": "Gerente Administrativa",
            "email": "mariaisabel@comercializadorarf.com",
            "phone": "+506 2234-7788", "whatsapp": "+506 8891-7788",
        },
        "opp": {
            "title": "Cotizaciones y facturación para Comercializadora Rodríguez",
            "description": "Módulo de cotizaciones y facturación para distribuidora con 8 vendedores. Flujo completo: lead → oportunidad → cotización → aprobación del cliente → factura electrónica.",
            "stage": "meeting_scheduled", "value": 3200.00,
            "close": date(2026, 9, 30), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Silvia Estela Mora Portuguez",
        "client": {
            "name": "Clínica Dental Mora",
            "industry": "Salud",
            "phone": "+506 2225-9900", "email": "citas@clinicadentalmora.cr",
            "website": "https://www.clinicadentalmora.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "Sabana Norte, Ave. Las Américas, Edificio Médico Dental, Consultorio 5",
            "status": "prospect", "tax_id": "3-101-556789",
        },
        "contact": {
            "full_name": "Silvia Estela Mora Portuguez",
            "position": "Directora y Odontóloga",
            "email": "smora@clinicadentalmora.cr",
            "phone": "+506 2225-9900", "whatsapp": "+506 8856-9900",
        },
        "opp": {
            "title": "Agenda y seguimiento de pacientes — Clínica Dental Mora",
            "description": "CRM para clínica dental: gestión de citas, historial clínico resumido por paciente, seguimiento de tratamientos de ortodoncia, recordatorios automáticos y control de pagos.",
            "stage": "meeting_scheduled", "value": 2600.00,
            "close": date(2026, 10, 5), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Rebeca Tatiana Blanco Vásquez",
        "client": {
            "name": "Consultoría RH Blanco & Partners",
            "industry": "Servicios de RRHH",
            "phone": "+506 2256-8877", "email": "info@rhblancopartners.com",
            "website": "https://www.rhblancopartners.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Barrio Escalante, Calle 33, Casa 45",
            "status": "prospect", "tax_id": "3-102-267890",
        },
        "contact": {
            "full_name": "Rebeca Tatiana Blanco Vásquez",
            "position": "Socia Directora",
            "email": "rblanco@rhblancopartners.com",
            "phone": "+506 2256-8877", "whatsapp": None,
        },
        "opp": {
            "title": "Pipeline comercial para firma de RRHH — Blanco & Partners",
            "description": "CRM para firma de recursos humanos: seguimiento de prospectos empresariales, propuestas de servicio, contratos de selección de personal y reportes de rentabilidad por proyecto.",
            "stage": "meeting_scheduled", "value": 2400.00,
            "close": date(2026, 10, 10), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Yolanda Esperanza Ruiz Pérez",
        "client": {
            "name": "Servicios de Limpieza Ruiz S.A.",
            "industry": "Servicios Empresariales",
            "phone": "+506 2277-3344", "email": "contratos@limpiezaruiz.cr",
            "website": "https://www.limpiezaruiz.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "San Francisco de Dos Ríos, Calle Los Arrayanes, Casa 8",
            "status": "prospect", "tax_id": "3-101-878901",
        },
        "contact": {
            "full_name": "Yolanda Esperanza Ruiz Pérez",
            "position": "Gerente General",
            "email": "yruiz@limpiezaruiz.cr",
            "phone": "+506 2277-3344", "whatsapp": "+506 8878-3344",
        },
        "opp": {
            "title": "Control de contratos corporativos — Servicios Ruiz Limpieza",
            "description": "CRM para empresa de limpieza: gestión de contratos recurrentes con clientes corporativos, programación de servicios, facturación mensual automática y alertas de renovación.",
            "stage": "meeting_scheduled", "value": 3000.00,
            "close": date(2026, 10, 15), "closed_at": None, "lost_reason": None,
        },
    },
    # ── CONTACTADO ────────────────────────────────────────────────────────────
    {
        "lead": "Sebastián Andrés Torres Chacón",
        "client": {
            "name": "Media Digital Torres",
            "industry": "Marketing y Publicidad",
            "phone": "+506 2211-4455", "email": "hola@mediatd.cr",
            "website": "https://www.mediatd.cr",
            "country": "Costa Rica", "city": "San José",
            "address": "Barrio La California, local junto al parque",
            "status": "prospect", "tax_id": "3-102-145678",
        },
        "contact": {
            "full_name": "Sebastián Andrés Torres Chacón",
            "position": "Fundador y Director Creativo",
            "email": "storres@mediatd.cr",
            "phone": "+506 2211-4455", "whatsapp": "+506 8801-4455",
        },
        "opp": {
            "title": "CRM de prospectos para agencia de marketing — Media Digital",
            "description": "Pipeline de prospectos para agencia de marketing digital: seguimiento de propuestas, control de proyectos activos por cliente, facturación mensual y dashboard de rentabilidad.",
            "stage": "contacted", "value": 2900.00,
            "close": date(2026, 10, 25), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Verónica Liliana Herrera Picado",
        "client": {
            "name": "Distribuciones VH S.A.",
            "industry": "Distribución y Logística",
            "phone": "+506 2255-3344", "email": "ventas@distribucionesVH.com",
            "website": "https://www.distribucionesVH.com",
            "country": "Costa Rica", "city": "San José",
            "address": "Alajuelita, Calle Principal, frente a la Bomba Delta",
            "status": "prospect", "tax_id": "3-101-612345",
        },
        "contact": {
            "full_name": "Verónica Liliana Herrera Picado",
            "position": "Propietaria y Gerente Comercial",
            "email": "vherrera@distribucionesVH.com",
            "phone": "+506 2255-3344", "whatsapp": "+506 8878-3344",
        },
        "opp": {
            "title": "Seguimiento de ventas con WhatsApp — Distribuciones VH",
            "description": "CRM con integración de WhatsApp para empresa distribuidora de productos de belleza. Control de vendedoras por zona, pedidos, comisiones y cartera de clientas.",
            "stage": "contacted", "value": 1900.00,
            "close": date(2026, 11, 1), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "lead": "Carlos Enrique Mora Vindas",
        "client": {
            "name": "Servicios Integrales Mora S.R.L.",
            "industry": "Consultoría",
            "phone": "+506 2244-3300", "email": "info@simora.cr",
            "website": "https://www.simora.cr",
            "country": "Costa Rica", "city": "Heredia",
            "address": "San Pablo de Heredia, frente a la Iglesia Católica",
            "status": "prospect", "tax_id": "3-102-589012",
        },
        "contact": {
            "full_name": "Carlos Enrique Mora Vindas",
            "position": "Gerente de Proyectos",
            "email": "cmora@simora.cr",
            "phone": "+506 2244-3300", "whatsapp": "+506 8823-3300",
        },
        "opp": {
            "title": "Pipeline de ventas para consultora — Servicios Integrales Mora",
            "description": "CRM con pipeline visual para equipo de 5 consultores comerciales. Módulos de leads, oportunidades, tareas de seguimiento y reportes semanales de avance.",
            "stage": "contacted", "value": 2500.00,
            "close": date(2026, 11, 10), "closed_at": None, "lost_reason": None,
        },
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 30% — 9 oportunidades desde clientes existentes (sin lead)
# ─────────────────────────────────────────────────────────────────────────────
CLIENT_OPPS = [
    {
        "client_partial": "Grupo Empresarial Alianza",
        "opp": {
            "title": "Renovación y ampliación de licencias CRM — Grupo Alianza",
            "description": "Expansión de la plataforma CRM para incorporar 10 usuarios adicionales. Incluye módulo de reportes ejecutivos avanzados, integración con Power BI y soporte prioritario anual.",
            "stage": "won", "value": 8500.00,
            "close": date(2026, 4, 30), "closed_at": datetime(2026, 4, 30, 11, 0),
            "lost_reason": None,
        },
    },
    {
        "client_partial": "Exportaciones Café Verde",
        "opp": {
            "title": "Módulo de trazabilidad de exportaciones — Café Verde S.A.",
            "description": "Desarrollo de módulo de trazabilidad integrado al CRM: seguimiento de lotes desde finca hasta cliente internacional, certificaciones de calidad, control de embarques y reportes por comprador.",
            "stage": "won", "value": 3900.00,
            "close": date(2026, 5, 15), "closed_at": datetime(2026, 5, 15, 16, 30),
            "lost_reason": None,
        },
    },
    {
        "client_partial": "Clínica de Salud Integral",
        "opp": {
            "title": "Acceso multiusuario y módulo de telemedicina — Clínica Bienestar",
            "description": "Ampliación del CRM para 5 usuarios adicionales de especialidades médicas. Incorporación de módulo de telemedicina: citas virtuales, fichas de teleconsulta y seguimiento de pacientes remotos.",
            "stage": "negotiation", "value": 6200.00,
            "close": date(2026, 8, 20), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Agencia Creativa Fusión",
        "opp": {
            "title": "Automatización de reportes y portal de clientes — Fusión Digital",
            "description": "Módulo de automatización de reportes mensuales para clientes de agencia. Portal self-service donde cada cliente visualiza sus KPIs en tiempo real. Integración con Google Analytics 4 y Meta Ads.",
            "stage": "negotiation", "value": 5100.00,
            "close": date(2026, 8, 30), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Constructora Los Pinos",
        "opp": {
            "title": "CRM de subcontratistas y proveedores — Constructora Los Pinos",
            "description": "Módulo de gestión de subcontratistas y proveedores integrado al CRM. Control de contratos, evaluación de desempeño, órdenes de servicio por proyecto y seguimiento de pagos.",
            "stage": "quote_sent", "value": 4800.00,
            "close": date(2026, 8, 10), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Cooperativa Agrícola",
        "opp": {
            "title": "Plataforma de asociados y trazabilidad — Coopvalle Central",
            "description": "Módulo de gestión de los 340 asociados: registro de fincas, producción entregada, liquidaciones, acceso móvil para asociados y reportes de trazabilidad del producto.",
            "stage": "diagnosis_done", "value": 3700.00,
            "close": date(2026, 9, 25), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Desarrolladora Residencial Palmares",
        "opp": {
            "title": "Integración CRM con sistema de cobros — Residencial Palmares",
            "description": "Integración del CRM con sistema de cobros de condominios. Sincronización de propietarios, estados de cuenta, alertas de morosidad y portal de pagos en línea.",
            "stage": "meeting_scheduled", "value": 4200.00,
            "close": date(2026, 10, 20), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Farmacéutica Nacional",
        "opp": {
            "title": "CRM para fuerza de ventas y licitaciones — Salud Total",
            "description": "CRM para el equipo de visitadores médicos y licitaciones públicas. Pipeline de instituciones de salud, seguimiento de propuestas a CCSS y MINSA, control de muestras y visitas.",
            "stage": "contacted", "value": 7500.00,
            "close": date(2026, 11, 15), "closed_at": None, "lost_reason": None,
        },
    },
    {
        "client_partial": "Hotel & Spa Las Brisas",
        "opp": {
            "title": "Módulo de grupos y eventos — Hotel Brisas del Atlántico",
            "description": "Módulo CRM para gestión de reservas de grupos corporativos y eventos especiales. Cotizaciones de paquetes, seguimiento de depósitos, control de servicios adicionales y reportes de ocupación.",
            "stage": "new", "value": 2800.00,
            "close": date(2026, 12, 1), "closed_at": None, "lost_reason": None,
        },
    },
]


async def main():
    conn = await asyncpg.connect(DB_URL)
    try:
        # ── 1. Borrar oportunidades existentes ────────────────────────────────
        deleted = await conn.fetchval("SELECT COUNT(*) FROM opportunities")
        await conn.execute("DELETE FROM opportunities")
        print(f"  Oportunidades anteriores eliminadas: {deleted}")

        # ── 2. Cargar leads ───────────────────────────────────────────────────
        lead_rows = await conn.fetch("SELECT id, full_name, email, phone, whatsapp FROM leads")
        leads_idx = {r["full_name"]: r for r in lead_rows}

        # ── 3. Cargar clientes existentes ─────────────────────────────────────
        client_rows = await conn.fetch("""
            SELECT c.id, c.name,
                   (SELECT ct.id FROM contacts ct
                    WHERE ct.client_id = c.id AND ct.is_primary = TRUE LIMIT 1) AS contact_id
            FROM clients c
        """)
        clients_idx = {r["name"]: {"id": r["id"], "contact_id": r["contact_id"]} for r in client_rows}

        def find_existing_client(partial):
            for name, data in clients_idx.items():
                if partial.lower() in name.lower():
                    return name, data
            raise ValueError(f"Cliente existente no encontrado: {partial!r}")

        inserted = 0

        async with conn.transaction():
            # ── 4. 70% — oportunidades desde leads ────────────────────────────
            print(f"\n  ── 70% OPORTUNIDADES DESDE LEADS (21) ──")
            for item in LEAD_OPPS:
                lead = leads_idx.get(item["lead"])
                if not lead:
                    print(f"  ⚠  Lead no encontrado: {item['lead']}")
                    continue

                c = item["client"]
                ct = item["contact"]
                o = item["opp"]

                # Crear cliente desde datos del lead
                client_id = uuid.uuid4()
                await conn.execute("""
                    INSERT INTO clients (id, name, client_type, industry, website, phone, email,
                        country, city, address, status, tax_id, owner_user_id)
                    VALUES ($1,$2,'company',$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                """,
                    client_id, c["name"], c["industry"], c.get("website"),
                    c["phone"], c["email"], c["country"], c["city"],
                    c.get("address"), c["status"], c["tax_id"], uuid.UUID(ADMIN_ID),
                )

                # Crear contacto primario (el lead mismo)
                contact_id = uuid.uuid4()
                await conn.execute("""
                    INSERT INTO contacts (id, client_id, full_name, position, email,
                        phone, whatsapp, is_primary, is_active)
                    VALUES ($1,$2,$3,$4,$5,$6,$7,TRUE,TRUE)
                """,
                    contact_id, client_id,
                    ct["full_name"], ct["position"], ct["email"],
                    ct["phone"], ct.get("whatsapp"),
                )

                # Insertar oportunidad
                await conn.execute("""
                    INSERT INTO opportunities (
                        id, client_id, contact_id, lead_id, title, description,
                        stage, estimated_value, probability, expected_close_date,
                        closed_at, owner_user_id, lost_reason
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
                """,
                    uuid.uuid4(), client_id, contact_id, lead["id"],
                    o["title"], o["description"], o["stage"],
                    o["value"], STAGE_PROB[o["stage"]],
                    o["close"], o.get("closed_at"), uuid.UUID(ADMIN_ID), o.get("lost_reason"),
                )

                inserted += 1
                tag = " ✓" if o["stage"] == "won" else (" ✗" if o["stage"] == "lost" else "")
                print(f"  [{inserted:02d}] {o['stage']:20s} ${o['value']:>8,.2f}  {c['name']}{tag}")

            # ── 5. 30% — oportunidades desde clientes existentes ──────────────
            print(f"\n  ── 30% OPORTUNIDADES DESDE CLIENTES EXISTENTES (9) ──")
            for item in CLIENT_OPPS:
                client_name, client_data = find_existing_client(item["client_partial"])
                o = item["opp"]

                await conn.execute("""
                    INSERT INTO opportunities (
                        id, client_id, contact_id, lead_id, title, description,
                        stage, estimated_value, probability, expected_close_date,
                        closed_at, owner_user_id, lost_reason
                    ) VALUES ($1,$2,$3,NULL,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                """,
                    uuid.uuid4(), client_data["id"], client_data["contact_id"],
                    o["title"], o["description"], o["stage"],
                    o["value"], STAGE_PROB[o["stage"]],
                    o["close"], o.get("closed_at"), uuid.UUID(ADMIN_ID), o.get("lost_reason"),
                )

                inserted += 1
                tag = " ✓" if o["stage"] == "won" else (" ✗" if o["stage"] == "lost" else "")
                print(f"  [{inserted:02d}] {o['stage']:20s} ${o['value']:>8,.2f}  {client_name}{tag}")

        # ── 6. Resumen ────────────────────────────────────────────────────────
        stats = await conn.fetch("""
            SELECT stage, COUNT(*) as n, SUM(estimated_value) as total
            FROM opportunities GROUP BY stage ORDER BY total DESC
        """)
        print(f"\n{'─'*60}")
        print(f"  {'Etapa':22s} {'#':>3}  {'Valor':>12}")
        print(f"{'─'*60}")
        grand = 0
        for s in stats:
            print(f"  {s['stage']:22s} {s['n']:>3}  ${float(s['total']):>10,.2f}")
            grand += float(s["total"])
        print(f"{'─'*60}")
        print(f"  {'TOTAL':22s} {inserted:>3}  ${grand:>10,.2f}")
        print(f"\n✓ {inserted} oportunidades insertadas (21 desde leads + 9 desde clientes).")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
