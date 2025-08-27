from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import combined_router
from app.database.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Anything that happens before the yield happens before the app starts
    await create_tables()

    yield

    # And anything that happens after the yield happens after the app stops
    return


app = FastAPI(
    title="Kohyli Bookstore",
    description="A simple API for a bookstore.",
    version="0.1.0",
    lifespan=lifespan,
    generate_unique_id_function=lambda route: route.name,
)

app.include_router(combined_router)
