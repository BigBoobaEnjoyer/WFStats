from app.handlers.players import router as players_router
from app.handlers.ping import router as ping_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

routers = [auth_router, players_router, user_router, ping_router]
