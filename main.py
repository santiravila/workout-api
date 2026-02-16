from fastapi import FastAPI
from features.routines.router import router as routines_router

app = FastAPI()

@app.get("/")
def root():
    return "This is the root"


app.include_router(routines_router)
