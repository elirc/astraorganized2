"""Translate expected boundary failures without returning submitted secrets or SQL."""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import StaleDataError


def install_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def invalid_request(_request, exc):
        return JSONResponse(
            status_code=422,
            content={
                "detail": [
                    {"loc": list(error["loc"]), "type": error["type"], "msg": error["msg"]}
                    for error in exc.errors()
                ]
            },
        )

    @app.exception_handler(IntegrityError)
    async def constraint_conflict(_request, _exc):
        return JSONResponse(
            status_code=409,
            content={"detail": "A uniqueness or reference constraint prevents this change"},
        )

    @app.exception_handler(StaleDataError)
    async def stale_write(_request, _exc):
        return JSONResponse(
            status_code=409,
            content={
                "detail": "This record changed. Reload it and review your draft before retrying"
            },
        )

    @app.exception_handler(OperationalError)
    async def database_unavailable(_request, _exc):
        return JSONResponse(
            status_code=503,
            content={"detail": "Database temporarily unavailable"},
            headers={"Retry-After": "1"},
        )
