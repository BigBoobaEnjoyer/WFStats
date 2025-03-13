from fastapi import FastAPI
from handlers.ping import router as ping_router
from handlers.players import router as players_router
app = FastAPI()


app.include_router(router=ping_router)
app.include_router(router=players_router)
