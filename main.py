from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from features.errors import DomainValidationError


def create_app():
    app = FastAPI()

    from features.routines.router import router as routines_router
    from features.sessions.router import router as sessions_router
    
    app.include_router(routines_router)
    app.include_router(sessions_router)

    @app.exception_handler(DomainValidationError)
    def domain_validation_exception_handler(request: Request, exc: DomainValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )

    @app.get("/")
    def root():
        return "This is the root"
    

    return app
