from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.use_cases.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app