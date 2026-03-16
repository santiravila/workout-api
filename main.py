from fastapi import FastAPI
from features.routines.router import router as routines_router
from features.sessions.router import router as sessions_router


app = FastAPI()


@app.get("/")
def root():
    return "This is the root"
    

app.include_router(routines_router)
app.include_router(sessions_router)
