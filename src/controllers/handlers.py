from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(KeyError)
    async def value_error_handler(request: Request, exc: KeyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "internal server error.",
                "details": str(exc)
            },
        )