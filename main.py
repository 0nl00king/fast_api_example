import uvicorn

from fastapi import (
    FastAPI,
    Request,
    status,
)

from fastapi.encoders import jsonable_encoder

from fastapi.exceptions import ValidationError

from fastapi.responses import JSONResponse

from fastapi.routing import APIRouter

from api.handlers.auth import auth_router
from api.handlers.user import user_router

from config import (
    APP_HOST,
    APP_PORT,
)

app = FastAPI(
    title="FastAPI Project API",
    description="A simple API for project",
    version="0.0.1",
)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(main_api_router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Благодаря этой функции клиент видит ошибки (ValidationError - Pydantic)
    происходящие на сервере, вместо 'Internal server error'
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
