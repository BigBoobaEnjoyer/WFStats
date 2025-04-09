from fastapi import FastAPI
import logging

from app.handlers import routers


app = FastAPI()
logging.basicConfig(level=logging.INFO)

for router in routers:
    app.include_router(router=router)

