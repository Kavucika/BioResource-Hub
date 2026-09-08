from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.categories import router as categories_router
from app.api.v1.resource import router as resources_router


app = FastAPI(
    title="BioResource Hub API",
    version="1.0.0"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    categories_router,
    prefix="/api/v1"
)

app.include_router(
    resources_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "message": "BioResource Hub API is running"
    }
