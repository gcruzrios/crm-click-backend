from fastapi import APIRouter

from app.api.v1 import (
    activities,
    auth,
    clients,
    config,
    contacts,
    leads,
    opportunities,
    quotes,
    reports,
    services,
    tasks,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(clients.router)
api_router.include_router(contacts.router)
api_router.include_router(leads.router)
api_router.include_router(opportunities.router)
api_router.include_router(services.router)
api_router.include_router(quotes.router)
api_router.include_router(tasks.router)
api_router.include_router(activities.router)
api_router.include_router(reports.router)
api_router.include_router(config.router)
