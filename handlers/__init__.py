from handlers.players import router as players_router
from handlers.ping import router as ping_router
from handlers.user import router as user_router
from handlers.auth import router as auth_router

routers = [auth_router, players_router, user_router, ping_router]
