from fastapi import FastAPI
from app.database import Base, engine
from app.api import auth, services, areas, about
from app.api.oauth import google, discord, github, microsoft
from app.core.scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
import app.services.timer.actions
import app.services.gmail.actions
import app.services.gmail.reactions
import app.services.google_drive.actions
import app.services.google_drive.reactions
import app.services.google_calendar.actions
import app.services.google_calendar.reactions
import app.services.google_sheets.reactions
import app.services.discord.actions
import app.services.discord.reactions
import app.services.openweather.actions
import app.services.github.actions
import app.services.outlook.actions
import app.services.outlook.reactions
import app.services.onedrive.reactions

_REGISTERED_SERVICES = [
    app.services.timer.actions,
    app.services.gmail.actions,
    app.services.gmail.reactions,
    app.services.google_drive.actions,
    app.services.google_drive.reactions,
    app.services.google_calendar.actions,
    app.services.google_calendar.reactions,
    app.services.google_sheets.reactions,
    app.services.discord.actions,
    app.services.discord.reactions,
    app.services.openweather.actions,
    app.services.github.actions,
    app.services.outlook.actions,
    app.services.outlook.reactions,
    app.services.onedrive.reactions,
]

api = FastAPI(title="AREA Backend")

origins = ["https://area-x5nk.onrender.com"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

api.include_router(auth.router)
api.include_router(google.router)
api.include_router(discord.router)
api.include_router(github.router)
api.include_router(microsoft.router)
api.include_router(services.router)
api.include_router(areas.router)
api.include_router(about.router)

start_scheduler()


@api.get("/")
def root():
    return {"status": "AREA backend running"}
