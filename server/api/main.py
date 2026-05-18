from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.routers import auth, characters, factions, npcs, progression, regions, sessions, ws

app = FastAPI(
    title="Hominun RPG API",
    version="0.1.0",
    description="Backend do RPG narrativo cooperativo inspirado na trilogia O Aprendiz.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "tauri://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=_PREFIX)
app.include_router(characters.router, prefix=_PREFIX)
app.include_router(regions.router, prefix=_PREFIX)
app.include_router(npcs.router, prefix=_PREFIX)
app.include_router(factions.router, prefix=_PREFIX)
app.include_router(progression.router, prefix=_PREFIX)
app.include_router(sessions.router, prefix=_PREFIX)
app.include_router(ws.router, prefix=_PREFIX)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": app.version}
