from fastapi import FastAPI

from db.database import engine, Base
from users import routers as user_routers

app = FastAPI()

app.include_router(user_routers.router)

@app.get("/")
async def home_page():
    return {"message": "welcome to online cinema"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)