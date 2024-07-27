from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes.user_routes import router as user_router
from routes.workout_routes import router as workout_router
from routes.nutrition_routes import router as nutrition_router
from routes.login import router as login_router
from security.authentication import Authenticate


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def read_health_check():
    return "Healthy", 200


@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")


app.include_router(login_router)
app.include_router(user_router, prefix="/api")
app.include_router(
    workout_router,
    prefix="/api",
    dependencies=[Depends(Authenticate.get_current_active_user)],
)
app.include_router(
    nutrition_router,
    prefix="/api",
    dependencies=[Depends(Authenticate.get_current_active_user)],
)
