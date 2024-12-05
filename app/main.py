from fastapi import FastAPI
from app.routers import router as router_students




app = FastAPI(title="PlanPro")

app.include_router(router_students)



<<<<<<< HEAD

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI authentication and authorization example"}







=======
>>>>>>> 06bd7fd2e8abd184b5468c9f06afe30b9d8f26c5
