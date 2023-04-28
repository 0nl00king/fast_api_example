from common import config
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from handlers.user import user_router
from handlers.auth import login_router


app = FastAPI(
    title="FastAPI Project API",
    description="A simple API for project",
    version="0.0.1",
)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
