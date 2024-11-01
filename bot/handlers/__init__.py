"""
Handles bot's commands
"""

from aiogram import Router

from . import common


def get_handlers_router() -> Router:
    """Returns a router with all the bot's commands"""
    router = Router()
    router.include_router(common.router)

    return router
