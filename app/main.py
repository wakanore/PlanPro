from fastapi import FastAPI
from app.routers import router as router_students




app = FastAPI(title="PlanPro")

app.include_router(router_students)




@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI authentication and authorization example"}







