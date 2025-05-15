from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.services.exceptions import ServiceError, NotFoundError, PermissionDeniedError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(_: Request, exc: PermissionDeniedError):
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ServiceError)
    async def service_error_handler(_: Request, exc: ServiceError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
