from aiogram import Router
from . import start, admin, application, admin_panel


def setup_routers() -> Router:
    r = Router()
    r.include_router(start.router)
    r.include_router(admin_panel.router)   # IsAdmin filter bilan
    r.include_router(admin.router)          # guruh tugmalari
    r.include_router(application.router)    # catch-all oxirida
    return r
