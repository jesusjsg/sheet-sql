from fastapi import APIRouter
from app.api.v1.routes import generate_sql

api_router = APIRouter()
api_router.include_router(generate_sql.router)
