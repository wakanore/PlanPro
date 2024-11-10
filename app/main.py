from fastapi import FastAPI
from app.routers import router as router_students

app = FastAPI(title="PlanPro")

app.include_router(router_students)


